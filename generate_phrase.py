import datetime as dt
from ollama import chat, ChatResponse
from calendar_scraper import get_upcoming_skips, get_target_work_week


def main():
    unformatted_start_date, unformatted_end_date = get_target_work_week()

    start_date = human_format_date(unformatted_start_date)
    end_date = human_format_date(unformatted_end_date)

    absent_list = generate_absent_list(get_upcoming_skips())

    if not absent_list:
        return
    
    print(absent_list)
    print(f'Call Script: {generate_phrase(start_date, end_date, absent_list)}')


def human_format_date(iso_date):
    return dt.datetime.fromisoformat(iso_date).strftime('%A, %B %d')


def file_format_date(iso_date):
    return dt.datetime.fromisoformat(iso_date).strftime('%m_%d')


def generate_phrase(start_date, end_date, absent_list):
    today = dt.datetime.now().strftime('%A, %B %d')

    with open('system_prompt_V2.txt', 'r') as file:
        SYSTEM_PROMPT = file.read()

    print('Generating phrase...')

    response: ChatResponse = chat(
        model='qwen3.5',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': f"""
             
            Skipper, here is the context for this week:

                Today's Date: {today}
                Upcoming School Week: {start_date} — {end_date}

                Absence(s) to report:
                {absent_list}

            Please generate the calling script based on the system instructions.
            
            """}
        ],
        think=False,
    )

    return response.message.content


def generate_absent_list(upcoming_skips):

    formatted_absences = []

    # Clean the dictionary data in the list to a Human-Readable Format
    for skip in upcoming_skips:
        formatted_date = dt.datetime.fromisoformat(skip['date']).strftime('%A, %B %d')
        formatted_absences.append({'name': skip['name'], 'date': formatted_date})

    absent_list_phrase = '\n'.join(f"• Date: {absence['date']}" for absence in formatted_absences)
    return absent_list_phrase


if __name__ == '__main__':
    main()