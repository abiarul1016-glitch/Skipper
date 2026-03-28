import calendar
import datetime as dt
from ollama import chat, ChatResponse
from calendar_scraper import get_upcoming_skips, get_target_work_week


def main():
    start_date, end_date = get_target_work_week()

    absent_list = generate_absent_list(get_upcoming_skips())

    if not absent_list:
        return
    
    print(absent_list)
    print(f'Call Script: {generate_phrase(start_date, end_date, absent_list)}')

def generate_phrase(start_date, end_date, absent_list):
    today = dt.datetime.now()
    today_weekday = calendar.day_name[today.weekday()]

    with open('system_prompt.txt', 'r') as file:
        SYSTEM_PROMPT = file.read()

    print('Generating phrase...')

    response: ChatResponse = chat(
        model='qwen3.5',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': f"""
             
            Skipper, here is the context for this week:

                Current Week: {start_date} — {end_date}
                Today's Date: {today}
                Current Day: {today_weekday}

                Absence(s) to report:
                {absent_list}

            Please generate the calling script based on the system instructions.
            
            """}
        ],
        think=False,
    )

    return response.message.content


def generate_absent_list(upcoming_skips):
    absent_list_phrase = '\n'.join(f"• Weekday: {calendar.day_name[skip['weekday']]}, Date: {skip['date']}" for skip in upcoming_skips)
    return absent_list_phrase


if __name__ == '__main__':
    main()