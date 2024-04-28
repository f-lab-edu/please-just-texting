from typing import Generator

from app.settings import settings
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = ("mysql+mysqldb://{username}:{password}@{host}:{port}/{dbname}").format(
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_host,
    port=settings.database_port,
    dbname=settings.database_name,
)

engine = create_engine(DATABASE_URL, echo=True)

session = sessionmaker(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = session()
    try:
        yield db
    finally:
        db.close()
