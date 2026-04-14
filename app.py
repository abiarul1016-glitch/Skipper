from flask import Flask, Response, request, send_from_directory
from twilio.twiml.voice_response import VoiceResponse

from calendar_scraper import get_target_work_week
from generate_phrase import file_format_date

app = Flask(__name__)

# GLOBAL VARIABLES
NGROK_URL = "https://incubous-caitlyn-herby.ngrok-free.dev"

# REMINDER: ADD SLASHES AT THE END OF DIRECTORY, SO FLASK CAN ENTER THEM
OUTPUT_FILE_DIRECTORY = "output_audios/"


# HOMEPAGE FOR SKIPPER
@app.route("/skipper/")
def index():
    return "This is the server hosting Skipper's required files."


# SERVES TWIML FOR SPECIFIC SCHOOL WEEK
@app.route("/skipper/xml", methods=["GET", "POST"])
def serve_twiML():
    # RETURNS DYNAMIC TWIML GENERATING BY CALCULATING THE UPCOMING SCHOOL WEEK
    response = VoiceResponse()

    # 1. EMBED THE FILENAME AND NGROK URL INTO TWIML
    audio_filepath = f"{NGROK_URL}/skipper/{OUTPUT_FILE_DIRECTORY}{get_filename()}"

    # 2. WAITING LOGIC - WAIT PAST SECOND RECORDING INSTRUCTION MESSAGE
    response.pause(length=20)

    # 3. USING ROUTE, LET TWILIO ACCESS THE SPECIFIC FILE
    response.play(url=audio_filepath)

    return Response(str(response), mimetype="text/xml")


# SERVES THE CUSTOM AUDIO
@app.route("/skipper/output_audios/<path:filename>")
def serve_audio(filename):
    # SAFELY RETURNS THE APPROPRIATE AUDIO FILE FOR THE WEEK
    return send_from_directory(OUTPUT_FILE_DIRECTORY, filename)


@app.route("/skipper/twilio-recording", methods=["GET", "POST"])
def get_twilio_recording():
    recording_url = request.values.get("RecordingUrl")
    recording_Sid = request.values.get("RecordingSid")

    # TODO: ADD FUNCTIONALITY TO DIRECTLY RETURN LINK/PRINT LINK IN MAIN.PY
    if recording_url:
        print(f"New recording available!: {recording_url}")

    # Have to return empty value to Twilio webhook, so it doesn't attempt to resend multiple times
    return "", 204


def get_filename():
    # 1. GET RELEVANT DATES FOR UPCOMING SCHOOL WEEK
    unformatted_start_date, unformatted_end_date = get_target_work_week()

    # 2. CALCULATE FILENAME
    file_start_date = file_format_date(unformatted_start_date)
    file_end_date = file_format_date(unformatted_end_date)

    output_filename = f"{file_start_date}-{file_end_date}.wav"
    return output_filename


if __name__ == "__main__":
    app.run(port=8000)
