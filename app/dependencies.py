from typing import Generator

from app.settings import settings
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

DATABASE_URL = ("mysql+asyncmy://{username}:{password}@{host}:{port}/{dbname}").format(
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_host,
    port=settings.database_port,
    dbname=settings.database_name,
)

engine = create_async_engine(DATABASE_URL, echo=True)

session = async_sessionmaker(bind=engine)


def get_db() -> Generator[AsyncSession, None, None]:
    db = session()
    try:
        yield db
    finally:
        db.close()
