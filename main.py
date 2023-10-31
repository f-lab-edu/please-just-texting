import os

import crud
import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Settings(BaseSettings):
    conf_debug: bool = True
    conf_host: str = "0.0.0.0"
    conf_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()


@app.get("/")
def read_root():
    return {"Hello": "World5"}


# CRUD
@app.get("/users/{user_id}")
def read_user(user_id: int):
    user = crud.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def run_app() -> None:
    uvicorn.run(
        "main:app",
        host=settings.conf_host,
        port=settings.conf_port,
        reload=settings.conf_debug,
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def main() -> None:
    run_app()


if __name__ == "__main__":
    main()
