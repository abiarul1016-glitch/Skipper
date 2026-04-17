"""
Skipper: Automated School Absence Call System

Generates and delivers pre-recorded phone calls to report student absences.
The system integrates with Google Calendar to fetch planned absences, uses LLM
to generate natural-sounding scripts, clones voice using Qwen TTS, and places
calls via Twilio.

Flow:
1. Scrape calendar for upcoming absences
2. Generate absence notification script using LLM
3. Synthesize script using voice cloning
4. Place call to school with recorded message
5. Optionally record the call for verification

Services:
- Flask API: Serves TwiML and audio files
- Ngrok: Creates secure tunnel for Twilio callbacks

Future Improvements:
- [ ] Convert server to FastAPI for better performance
- [ ] Implement automatic call recording retrieval
- [ ] Stream audio live instead of pre-generating files
- [ ] Add machine detection to avoid wait times
- [ ] Improve LLM prompt for more dynamic responses
"""

import subprocess
import time

from twilio.rest import Client

from calendar_scraper import get_target_work_week, get_upcoming_skips
from config import Config
from generate_audio import generate_audio
from generate_phrase import (
    file_format_date,
    generate_absent_list,
    generate_phrase,
    human_format_date,
)


def main():
    """
    Execute the absence notification workflow.

    Steps:
    1. Fetch planned absences from calendar
    2. Generate call script using LLM
    3. Synthesize audio with voice cloning
    4. Place Twilio call to school
    5. Record call if enabled
    """
    print("Hello from skipper!\n")

    # Fetch planned absences for the current work week
    upcoming_skips = get_upcoming_skips(Config.SKIP_CALENDAR_ID)

    # Calculate week bounds and format for display
    unformatted_start_date, unformatted_end_date = get_target_work_week()
    start_date = human_format_date(unformatted_start_date)
    end_date = human_format_date(unformatted_end_date)

    # Check if there are any absences to report
    absent_list = generate_absent_list(upcoming_skips)

    if not absent_list:
        print("No absences this week!")
        return

    print("PLANNED ABSENCES THIS WEEK:")
    print(absent_list)

    # Generate natural-sounding script for the call
    print()
    generated_phrase = generate_phrase(
        start_date, end_date, absent_list, ollama_model=Config.OLLAMA_MODEL
    )

    print(f"\nCall Script: {generated_phrase}\n")

    # Synthesize audio using voice cloning
    file_start_date = file_format_date(unformatted_start_date)
    file_end_date = file_format_date(unformatted_end_date)

    output_filename = (
        f"{Config.OUTPUT_FILE_DIRECTORY}/{file_start_date}-{file_end_date}.wav"
    )

    generate_audio(
        reference_audio=str(Config.REF_AUDIO_PATH),
        reference_audio_transcript=str(Config.REF_AUDIO_TRANSCRIPT),
        output_file=output_filename,
        text_to_generate=generated_phrase,
        tts_model=Config.TTS_MODEL,
    )

    # Place the call to school
    client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

    if Config.RECORDING:
        # Test mode: record call for verification
        call = client.calls.create(
            record=True,
            recording_channels="dual",
            recording_status_callback=f"{Config.NGROK_URL}/skipper/twilio-recording",
            recording_status_callback_event="completed",
            send_digits=Config.SEND_DIGITS,
            to=Config.TO_NUMBER,
            from_=Config.FROM_NUMBER,
            url=f"{Config.NGROK_URL}/skipper/xml",
        )
    else:
        # Production mode: place call without recording
        call = client.calls.create(
            send_digits=Config.SEND_DIGITS,
            to=Config.TO_NUMBER,
            from_=Config.FROM_NUMBER,
            url=f"{Config.NGROK_URL}/skipper/xml",
        )

    print(
        f"🎉 Call placed to: {Config.TO_NUMBER}, from: {Config.FROM_NUMBER}! Call SID: {call.sid}"
    )


def start_services() -> tuple:
    """
    Start Flask server and Ngrok tunnel in background processes.

    Creates a logs directory and redirects subprocess output to files to keep
    the main terminal clean.

    Returns:
        tuple: (server_process, tunnel_process, flask_log_file, ngrok_log_file)
    """
    # Create logs directory for service output
    logs_dir = Config.PROJECT_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Prepare log files
    flask_log = open(logs_dir / "flask.log", "w")
    ngrok_log = open(logs_dir / "ngrok.log", "w")

    # Start Flask server on configured port
    server: subprocess.Popen = subprocess.Popen(
        ["uv", "run", "app.py"],
        stdout=flask_log,
        stderr=flask_log,
    )
    time.sleep(Config.SERVICE_START_TIMEOUT)

    # Start Ngrok tunnel to expose server to internet
    tunnel: subprocess.Popen = subprocess.Popen(
        ["ngrok", "http", str(Config.FLASK_PORT)],
        stdout=ngrok_log,
        stderr=ngrok_log,
    )
    time.sleep(Config.SERVICE_START_TIMEOUT)

    print("✅ Flask server started (logs: logs/flask.log)")
    print("✅ Ngrok tunnel started (logs: logs/ngrok.log)")

    return server, tunnel, flask_log, ngrok_log


if __name__ == "__main__":
    """Entry point: Start services and run absence notification workflow."""
    server, tunnel, flask_log, ngrok_log = start_services()

    print()

    try:
        print("Services started, running main script...")
        main()
    finally:
        # Clean shutdown: stop services and close log files
        server.terminate()
        tunnel.terminate()
        flask_log.close()
        ngrok_log.close()
