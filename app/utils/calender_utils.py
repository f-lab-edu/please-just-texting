import datetime
import logging
import os
import pickle

from app.settings import PROJECT_ROOT
from app.settings import settings
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger()

SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]
USER_TO_IMPERSONATE = settings.impersonation_account


def get_calendar_service() -> Request:
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject=USER_TO_IMPERSONATE
    )
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
