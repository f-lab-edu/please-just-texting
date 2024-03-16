import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

session = sessionmaker(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = session()
    try:
        yield db
    finally:
        db.close()
