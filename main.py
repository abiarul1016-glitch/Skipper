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
SECRETS_FILE_PATH = "/Users/abishanarulselvan/CODING/snyder_pranker/secrets.env"
load_dotenv(SECRETS_FILE_PATH)

SKIP_CALENDAR_ID = "2cab442dcaa371859cc8c0137d96f06d48b4d2e85ee67d5ee8a505f18f74b357@group.calendar.google.com"

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

# SYSTEM PROMPT
# SYSTEM_PROMPT_PATH = "/Users/abishanarulselvan/CODING/snyder_pranker/system_prompts/april_fools/april_fools_V2.txt"

# FILE VARIABLES
NGROK_URL = "https://incubous-caitlyn-herby.ngrok-free.dev"
OUTPUT_FILE_DIRECTORY = "/Users/abishanarulselvan/CODING/Skipper/output_audios"


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
    generated_phrase = generate_phrase(start_date, end_date, absent_list)

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
    )

    # 4. USE TWILIO TO PLACE THE CALL, DIAL ONE, AND PLAY THE AUDIO, AND HANG UP
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.calls.create(
        url="https://incubous-caitlyn-herby.ngrok-free.dev/skipper.xml",
        to=MY_PHONE_NUMBER,
        # USE ONLY IN PRODUCTION
        # to=SCHOOL_PHONE_NUMBER,
        from_=DAD_PHONE_NUMBER,
    )


if __name__ == "__main__":
    main()
