"""Google Calendar integration for fetching absence events.

Authenticates with Google Calendar API and retrieves absence events
for the current school week from the configured SKIP calendar.
"""

import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import Config

# Google Calendar API scopes - readonly for this application
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
    """Test calendar scraping by fetching and printing upcoming absences."""
    upcoming_skips = get_upcoming_skips(Config.SKIP_CALENDAR_ID)

    if upcoming_skips:
        for skip in upcoming_skips:
            print(f"{skip['name']}: {skip['date']} - {skip['weekday']}")


def get_skip_calendar_id():
    """TODO: Implement automatic calendar ID discovery from calendar list."""
    pass


def get_upcoming_skips(skip_calendar: str = None):
    """Fetch all absence events for the current school week.

    Queries the configured SKIP calendar for events between the start and end
    of the current work week.

    Args:
        skip_calendar: Calendar ID to query (uses Config default if None)

    Returns:
        list: List of dicts with keys: name, date, weekday

    Raises:
        HttpError: If Google Calendar API request fails
    """
    if skip_calendar is None:
        skip_calendar = Config.SKIP_CALENDAR_ID

    creds = None

    # Load cached credentials or authenticate user
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh expired credentials
            creds.refresh(Request())
        else:
            # Run OAuth flow for first-time authentication
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Cache credentials for future use
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Get the target work week bounds
        time_min, time_max = get_target_work_week()

        print("📅 Fetching absence events from SKIP calendar...\n")

        # Query calendar API for events in the work week
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

        # Parse event data into list of dicts
        upcoming_skips = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            weekday = dt.datetime.fromisoformat(start).weekday()

            upcoming_skips.append(
                {"name": event["summary"], "date": start, "weekday": weekday}
            )

        return upcoming_skips

    except HttpError as error:
        print(f"❌ Calendar API error: {error}")


def get_target_work_week() -> tuple:
    """Calculate the start and end dates of the current school work week.

    If today is a weekday (Mon-Fri): returns today through Friday.
    If today is a weekend (Sat-Sun): returns the next Monday through Friday.

    Returns:
        tuple: (time_min, time_max) as ISO 8601 strings with UTC timezone
    """
    today = dt.datetime.now()
    weekday = today.weekday()

    if weekday == 5 or weekday == 6:
        # If today is weekend, schedule for next week's Monday-Friday
        days_until_monday = 7 - weekday
        start_date = today + dt.timedelta(days=days_until_monday)
        end_date = start_date + dt.timedelta(days=4)
    else:
        # If weekday, schedule from today through Friday
        start_date = today
        days_until_friday = 4 - weekday
        end_date = today + dt.timedelta(days=days_until_friday)

    time_min = start_date.replace(hour=0, minute=0, second=0).isoformat() + "Z"
    time_max = end_date.replace(hour=23, minute=59, second=59).isoformat() + "Z"

    return time_min, time_max


if __name__ == "__main__":
    main()
