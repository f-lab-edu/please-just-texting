import json
import os

import schemas
import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from settings import settings
from utils import calender_utils
from utils import openai_utils

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("dialogue_form.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
async def submit_dialogue(
    request: Request, username: str = Form(...), message: str = Form(...)
) -> None:
    schedule_response = openai_utils.getResponseFromOpenai(message)
    parsed_response = json.loads(schedule_response)

    calender_utils.add_event_to_calendar(parsed_response)

    return templates.TemplateResponse(
        "show_response.html",
        {"request": request, "data": parsed_response},
    )


def run_app() -> None:
    uvicorn.run(
        "main:app",
        host=settings.conf_host,
        port=settings.conf_port,
        reload=settings.conf_debug,
    )


def main() -> None:
    run_app()


if __name__ == "__main__":
    main()
