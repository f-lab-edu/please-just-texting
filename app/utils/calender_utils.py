import datetime
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 캘린더 API 접근 권한 설정
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service() -> Resource:
    creds = None
    # lode token file
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # Create new credentials if they are invalid or do not exist
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the new credentials to the token.pickle file
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)
    return service


def add_event_to_calendar(date: date, title: str, description: str) -> None:
    service = get_calendar_service()

    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": f"{date}T09:00:00",
            "timeZone": "Asia/Seoul",
        },
        "end": {
            "dateTime": f"{date}T10:00:00",
            "timeZone": "Asia/Seoul",
        },
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")
