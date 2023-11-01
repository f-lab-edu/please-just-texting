import os.path
import pickle

import datatime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# google calendar api setting
SCOPES = ["https://www.googleapis.com/auth/calendar"]

creds = None
if os.path.exists("token.pickle"):
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "path_to_your_client_secrets.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

# google calendar api object
service = build("calendar", "v3", credentials=creds)

event = {
    "summary": "테스트 일정",
    "description": "Google Calendar API를 사용한 테스트 일정",
    "start": {
        "dataTime": "2023-11-05T09:00:00-07:00",
        "timeZone": "Asia/Seoul",
    },
    "end": {
        "dateTime": "2023-11-05T10:00:00-07:00",
        "timeZone": "Asia/Seoul",
    },
}

event = service.events().insert(calendarID="primary", body=event).execute()
print(f'일정 추가되었습니다: {event["htmlLink"]}')
