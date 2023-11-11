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

# from crud import get_user

app = FastAPI()
# DATABASE_URL = os.environ.get("DATABASE_URL")
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# template
templates = Jinja2Templates(directory="templates")


class Settings(BaseSettings):
    conf_debug: bool = True
    conf_host: str = "0.0.0.0"
    conf_port: int = 8000
    openai_api_key: str = None
    conversation: str = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()


@app.get("/dialogue-form", response_class=HTMLResponse)
async def get_dialogue_form(request: Request):
    return templates.TemplateResponse("dialogue_form.html", {"request": request})


@app.post("/submit-dialogue")
async def submit_dialogue(dialogue: str = Form(...)):
    return {"dialogue": dialogue}


def run_app() -> None:
    uvicorn.run(
        "main:app",
        host=settings.conf_host,
        port=settings.conf_port,
        reload=settings.conf_debug,
    )


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


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
