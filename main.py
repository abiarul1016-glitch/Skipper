# GREATEST IMPROVEMENT: TODO: AUTOMATICALLY LAUNCHING FLASKSERVER AND NGROK, WHEN MAIN.PY IS RAN, SO I DON'T MANUALLY NEED TO DO IT

# 1. TODO: MAYBE CONVERT THE SERVER CODE TO FASTAPI
# 2. TODO: IMPLEMENT A FUNCTIONALITY, SO THAT THE RECORDING URL IS REQUESTED ONCE IT IS COMPLEMENTED (ONLY IF CALL WAS RECORDED), MIGHT NEED TO TAKE USER INPUT IF THEY WANT TO RECORD CALL, BUT THIS MAY BE ANNOYING TO ASK EVERYTIME.
# 3. TODO: MAYBE USE FASTAPI TO STREAM THE AUDIO SO THE APP IS MUCH MORE PERFORMANT
# THE URL WILL THEN HAVE TO HIT A TWIML WHICH WAITS A COUPLE SECONDS TO BYPASS THE INSTRUCTORY MESSAGE, AND THEN USES THE STREAM KEYWORD TO STREAM AUDIO LIVE, FROM A BUFFER
# DUE TO THE IMMENSE WAITING THAT OCCURS, THE BUFFER WILL LIKELY BE FILLED, MAKING THIS VERY EFFICIENT SAVING A COUPLE OF SECONDS.
# 4. TODO: IMPROVE SYSTEM PROMPT TO STOP ALWAYS CHOOSING FAMILY COMMITMENT TO STAY MORE DYNAMIC

import os

from dotenv import load_dotenv
from twilio.rest import Client

from calendar_scraper import get_target_work_week, get_upcoming_skips
from generate_audio import REFERENCE_AUDIO_TRANSCRIPT, generate_audio
from generate_phrase import (
    file_format_date,
    generate_absent_list,
    generate_phrase,
    human_format_date,
)

# GLOBAL VARIABLES
SECRETS_FILE_PATH = "/Users/abishanarulselvan/CODING/Skipper/secrets.env"
load_dotenv(SECRETS_FILE_PATH)

SKIP_CALENDAR_ID = os.getenv("SKIP_CALENDAR_ID")

# REF AUDIO VARIABLES
REF_AUDIO_PATH = "reference_audios/appa_reference.wav"
REF_AUDIO_TRANSCRIPT = "reference_audios/appa_reference.txt"

# TWILIO VARIABLES
ACCOUNT_SID: str | None = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN: str | None = os.getenv("TWILIO_AUTH_TOKEN")

MY_PHONE_NUMBER: str | None = os.getenv("MY_PHONE_NUMBER")
TWILIO_PHONE_NUMBER: str | None = os.getenv("TWILIO_PHONE_NUMBER")

# REQUIRED PHONE NUMBERS
DAD_PHONE_NUMBER = os.getenv("DAD_PHONE_NUMBER")
SCHOOL_PHONE_NUMBER = os.getenv("SCHOOL_PHONE_NUMBER")

# LLM VARIABLES
# NOTE: ADD PATH - SYSTEM_PROMPT_PATH = ".txt", IMPROVE THE PROMPT AS WELL
OLLAMA_MODEL = "qwen3.5"  # use 'gemma4' for the other installed model
TTS_MODEL = "mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16"  # Replace 1.7, with 0.6 to use the smaller + faster model

# FILE VARIABLES
NGROK_URL = "https://incubous-caitlyn-herby.ngrok-free.dev"
OUTPUT_FILE_DIRECTORY = "/Users/abishanarulselvan/CODING/Skipper/output_audios"

# SELECTION VARIABLES

# NUMBER SELECTION
FROM_NUMBER = DAD_PHONE_NUMBER
TO_NUMBER = SCHOOL_PHONE_NUMBER

# RECORDING SELECTION - USE FOR TESTING PURPOSES
RECORDING = os.getenv("RECORDING") == "True"


def main():

    print("Hello from skipper!\n")

    # 1. SCRAPE CALENDAR TO SEE PLANNED ABSENCES
    upcoming_skips = get_upcoming_skips()

    # 2. CALL LLM TO GENERATE PHRASE FOR CALL CONSIDERING ABSENT DAYS, WHILE FOLLOWING PARAMETERS
    unformatted_start_date, unformatted_end_date = get_target_work_week()
    start_date = human_format_date(unformatted_start_date)
    end_date = human_format_date(unformatted_end_date)

    absent_list = generate_absent_list(upcoming_skips)

    if not absent_list:
        print("No absences this week!")
        return

    print("PLANNED ABSENCES THIS WEEK:")
    print(absent_list)

    print()
    generated_phrase = generate_phrase(
        start_date, end_date, absent_list, ollama_model=OLLAMA_MODEL
    )

    print(f"\nCall Script: {generated_phrase}\n")

    # 3. GENERATE AUDIO USING CLONED VOICE
    file_start_date = file_format_date(unformatted_start_date)
    file_end_date = file_format_date(unformatted_end_date)

    output_filename = f"{OUTPUT_FILE_DIRECTORY}/{file_start_date}-{file_end_date}.wav"

    generate_audio(
        reference_audio=REF_AUDIO_PATH,
        reference_audio_transcript=REFERENCE_AUDIO_TRANSCRIPT,
        output_file=output_filename,
        text_to_generate=generated_phrase,
        tts_model=TTS_MODEL,
    )

    # 4. USE TWILIO TO PLACE THE CALL, DIAL ONE, AND PLAY THE AUDIO, AND HANG UP
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # TODO: TRY TO IMPLEMENT AUTOMATED MACHINE DETECTION (IT IS OVERRIDDEN BY SENDDIGITS), SO WAITING VALUES IN XML NEED NOT BE HARDCODED

    # RECORDING VERSION ONLY FOR TEST PURPOSES
    if RECORDING:
        call = client.calls.create(
            record=True,
            recording_channels="dual",
            recording_status_callback=f"{NGROK_URL}/skipper/twilio-recording",
            recording_status_callback_event="completed",
            send_digits="WWWWWWW1",
            to=TO_NUMBER,
            from_=FROM_NUMBER,
            url=f"{NGROK_URL}/skipper/xml",
        )

    else:
        # NORMAL, AND COMMON USE CASE EDITION
        call = client.calls.create(
            send_digits="WWWWWWW1",
            to=TO_NUMBER,
            from_=FROM_NUMBER,
            url=f"{NGROK_URL}/skipper/xml",
        )

    # 5. SIMPLE SUCCESS LOG
    print(f"🎉 Call placed to: {TO_NUMBER}, from: {FROM_NUMBER}! Call SID: {call.sid}")

    # TODO: 6. USE REQUESTS (OR SOMETHING) TO EXTRACT THE RECORDING URL FROM THE FLASK APP, TO KEEP EVERYTHING CENTRALIZED WITHIN MAIN.PY FOR EASE OF USE


if __name__ == "__main__":
    main()
