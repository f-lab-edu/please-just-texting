import datetime
import logging
import os
import pickle

from app.settings import PROJECT_ROOT
from googleapiclient.discovery import build

logger = logging.getLogger()

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    creds = None
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
