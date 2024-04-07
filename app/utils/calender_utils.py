import datetime
import logging
import os
import pickle

from app.settings import PROJECT_ROOT
from googleapiclient.discovery import build

"""
============================================================
Replaced on: 2024-4-7
The current application does not use a web browser.
It's impossible to perform authentication via the conventional OAuth 2.0 method.
For future changes, leave code with comments.

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
============================================================
"""


logger = logging.getLogger()

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    creds = None

    """
    ============================================================
    Replaced on: 2024-4-7
    The current application does not use a web browser.
    It's impossible to perform authentication via the conventional OAuth 2.0 method.
    For future changes, leave code with comments.

    token_path = PROJECT_ROOT / "token.pickle"
    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    ============================================================
    """

    service = build("calendar", "v3", credentials=creds)
    return service


def add_event_to_calendar(parsed_response: dict[str, str]) -> None:
    service = get_calendar_service()

    title = parsed_response["title"]
    date = parsed_response["date"]
    description = parsed_response["description"]

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
    logger.debug(f"Event created: {event.get('htmlLink')}")
