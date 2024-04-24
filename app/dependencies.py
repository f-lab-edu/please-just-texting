import os
from typing import Generator

from app.settings import settings
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = f"mysql+mysqldb://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
engine = create_engine(DATABASE_URL, echo=True)

session = sessionmaker(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = session()
    try:
        yield db
    finally:
        db.close()
