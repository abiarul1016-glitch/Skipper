from calendar_scraper import get_target_work_week, get_upcoming_skips
from generate_phrase import human_format_date, file_format_date, generate_absent_list, generate_phrase
from generate_audio import generate_audio

SKIP_CALENDAR_ID = '2cab442dcaa371859cc8c0137d96f06d48b4d2e85ee67d5ee8a505f18f74b357@group.calendar.google.com'

REFERENCE_AUDIO = 'reference_audios/appa_reference.wav'
REFERENCE_AUDIO_TRANSCRIPT = 'reference_audios/appa_reference.txt'
OUTPUT_FILEPATH = 'output_audios/'

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
        print('No absences this week!')
        return
    
    print('PLANNED ABSENCES THIS WEEK:')
    print(absent_list)

    print()
    generated_phrase = generate_phrase(start_date, end_date, absent_list)

    print(f'\nCall Script: {generated_phrase}\n')

    # 3. GENERATE AUDIO USING CLONED VOICE
    file_start_date = file_format_date(unformatted_start_date)
    file_end_date = file_format_date(unformatted_end_date)

    output_filename = f'{OUTPUT_FILEPATH}{file_start_date}-{file_end_date}.wav'

    generate_audio(
        reference_audio=REFERENCE_AUDIO,
        reference_audio_transcript=REFERENCE_AUDIO_TRANSCRIPT,
        output_file=output_filename,
        text_to_generate=generated_phrase)

    # 4. USE TWILIO TO PLACE THE CALL, DIAL ONE, AND PLAY THE AUDIO, AND HANG UP

if __name__ == "__main__":
    main()
