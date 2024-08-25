from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


def get_session():
    from app.settings import settings
    from dotenv import load_dotenv

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
    return session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = get_session()
    db = session()
    try:
        yield db
    finally:
        await db.close()
