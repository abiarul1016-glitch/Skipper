"""Flask API server for Skipper.

Serves TwiML for Twilio calls and audio files for playback.
Acts as an intermediary between Twilio and the audio generation system.
"""

from flask import Flask, Response, request, send_from_directory
from twilio.twiml.voice_response import VoiceResponse

from calendar_scraper import get_target_work_week
from config import Config
from generate_phrase import file_format_date

app = Flask(__name__)


@app.route("/skipper/")
def index():
    """Health check endpoint."""
    return "This is the server hosting Skipper's required files."


@app.route("/skipper/xml", methods=["GET", "POST"])
def serve_twiML():
    """Generate TwiML response with audio playback for Twilio call.

    Pauses to skip past school's automated instructions, then plays
    the pre-recorded absence notification message.
    """
    response = VoiceResponse()

    # Get audio file for current week
    audio_filepath = f"{Config.NGROK_URL}/skipper/output_audios/{get_filename()}"

    # Skip school's automated instructions (configurable pause)
    response.pause(length=Config.PAUSE_SECONDS)

    # Play the absence notification audio
    response.play(url=audio_filepath)

    return Response(str(response), mimetype="text/xml")


@app.route("/skipper/output_audios/<path:filename>")
def serve_audio(filename):
    """Serve audio file for playback.

    Args:
        filename: Audio file to stream
    """
    return send_from_directory(str(Config.OUTPUT_FILE_DIRECTORY), filename)


@app.route("/skipper/twilio-recording", methods=["GET", "POST"])
def get_twilio_recording():
    """Handle Twilio recording status callback.

    Called when a recorded call completes. Currently logs the recording URL;
    TODO: implement retrieval in main.py for centralized handling.
    """
    recording_url = request.values.get("RecordingUrl")
    recording_sid = request.values.get("RecordingSid")

    if recording_url:
        print(f"📹 Call recorded: {recording_url}")

    # Return 204 to prevent Twilio from retrying
    return "", 204


def get_filename():
    """Get audio filename for the current school week.

    Returns:
        str: Filename in format YYYY-MM-DD-YYYY-MM-DD.wav
    """
    unformatted_start_date, unformatted_end_date = get_target_work_week()
    file_start_date = file_format_date(unformatted_start_date)
    file_end_date = file_format_date(unformatted_end_date)
    return f"{file_start_date}-{file_end_date}.wav"


if __name__ == "__main__":
    """Start Flask server on configured port."""
    app.run(port=Config.FLASK_PORT)
