import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

SKIP_CALENDAR_ID = "2cab442dcaa371859cc8c0137d96f06d48b4d2e85ee67d5ee8a505f18f74b357@group.calendar.google.com"


def main():
    upcoming_skips = get_upcoming_skips()

    # FOR TESTING REASONS

    if upcoming_skips:
        for skip in upcoming_skips:
            print(f"{skip['name']}: {skip['date']} - {skip['weekday']}")
            # print(skip['name'], skip['date'], skip['weekday'])


def get_skip_calendar_id():
    # Checks environment if calendar id is given, and if not checks through calendar for relevant calendar ID
    ...


def get_upcoming_skips(skip_calendar: str = SKIP_CALENDAR_ID):

    # Implement function to get SKIP Calendar ID based on Calendar name (SKIP) from Calendar list,
    # if the id is not provided by user in environment—for now this is fine
    skip_calendar = SKIP_CALENDAR_ID

    """
  Gets all upcoming skips for the upcoming school week
  """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Filter out events for the relevant work week
        time_min, time_max = get_target_work_week()

        # Call the Calendar API
        print("🚀 Getting the upcoming SKIP events for upcoming school week...\n")

        events_result = (
            service.events()
            .list(
                calendarId=skip_calendar,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming SKIP events found.")
            return

        # Cleans the data to put in dictionary with only relevant information
        upcoming_skips = []

        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            weekday = dt.datetime.fromisoformat(start).weekday()

            upcoming_skips.append(
                {"name": event["summary"], "date": start, "weekday": weekday}
            )

        return upcoming_skips

    except HttpError as error:
        print(f"An error occurred: {error}")


def get_target_work_week() -> tuple:
    """
    Logic which finds the upcoming work week depending on whether today's date is part of
    the upcoming work week

    NEED TO UPDATE THIS AS THE PROGRAM IS LIKELY TO BE RAN ON THE WEEKDAY OF THE RELEVANT SCHOOL WEEK
    Just will have to reverse the logic

    """
    today = dt.datetime.now()
    weekday = today.weekday()

    if weekday == 5 or weekday == 6:
        #   If today is the weekend apply the program on upcoming work week
        days_until_monday = 7 - weekday
        start_date = today + dt.timedelta(days=days_until_monday)

        # End date span is always the Friday of the same week
        end_date = start_date + dt.timedelta(days=4)
    else:
        #   If it's any other day of the week, start_date is the same day, until the end of the week

        start_date = today
        days_until_friday = 4 - weekday
        end_date = today + dt.timedelta(days=days_until_friday)

    time_min = start_date.replace(hour=0, minute=0, second=0).isoformat() + "Z"
    time_max = end_date.replace(hour=23, minute=59, second=59).isoformat() + "Z"

    return time_min, time_max


if __name__ == "__main__":
    main()
