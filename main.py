from calendar_scraper import get_target_work_week, get_upcoming_skips
from generate_phrase import generate_absent_list, generate_phrase
from generate_audio import generate_audio

SKIP_CALENDAR_ID = '2cab442dcaa371859cc8c0137d96f06d48b4d2e85ee67d5ee8a505f18f74b357@group.calendar.google.com'

REFERENCE_AUDIO = 'reference_audios/appa_reference.wav'
REFERENCE_AUDIO_TRANSCRIPT = 'reference_audios/appa_reference.txt'
OUTPUT_FILEPATH = 'output_audios/'

def main():

    print("Hello from skipper!")

    # 1. SCRAPE CALENDAR TO SEE PLANNED ABSENCES
    upcoming_skips = get_upcoming_skips()

    # 2. CALL LLM TO GENERATE PHRASE FOR CALL CONSIDERING ABSENT DAYS, WHILE FOLLOWING PARAMETERS
    start_date, end_date = get_target_work_week()

    absent_list = generate_absent_list(upcoming_skips)

    if not absent_list:
        return
    
    print(absent_list)


    generated_phrase = generate_phrase(start_date, end_date, absent_list)

    print(f'Call Script: {generated_phrase}')

    # 3. GENERATE AUDIO USING CLONED VOICE
    output_filename = f'{OUTPUT_FILEPATH}{start_date}-{end_date}.wav'
    
    generate_audio(
        reference_audio=REFERENCE_AUDIO,
        reference_audio_transcript=REFERENCE_AUDIO_TRANSCRIPT,
        output_file=output_filename,
        text_to_generate=generated_phrase)

    # 4. USE TWILIO TO PLACE THE CALL, DIAL ONE, AND PLAY THE AUDIO, AND HANG UP

if __name__ == "__main__":
    main()
