import json
import os

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
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from utils import calender_utils
from utils import openai_utils

# from crud import get_user

app = FastAPI()


# DATABASE_URL = os.environ.get("DATABASE_URL")
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# template
templates = Jinja2Templates(directory="app/templates")


class Settings(BaseSettings):
    conf_debug: bool = True
    conf_host: str = "0.0.0.0"
    conf_port: int = 8000
    openai_api_key: str = None
    conversation: str = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()


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


# TODO: {I've temporarily commented the database code while testing the calendar and OpenAI function. Once I verify these work, I'll de-comment the database code}
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# TODO: {I've temporarily commented the database code while testing the calendar and OpenAI function. Once I verify these work, I'll de-comment the database code}
# # CRUD
# @app.get("/users/{user_id}")
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     user = get_user(db, user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


def main() -> None:
    run_app()


if __name__ == "__main__":
    main()
