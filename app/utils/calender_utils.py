import datetime
import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 캘린더 API 접근 권한 설정
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    creds = None
    # lode token file
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # 자격증명이 유효하지 않거나 존재하지 않으면 새로 생성
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # 새로운 자격증명을 token.pickle 파일에 저장
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)
    return service


def add_event_to_calendar(date, title, description):
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
