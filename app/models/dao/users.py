from app.models.base import User
from app.schemas import UpdateUser
from app.schemas import UserCreate
from app.schemas import UserSignin
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import delete
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_db_user(db: AsyncSession, field):
    statement = select(User).where(or_(User.name == field, User.email == field))
    result = await db.execute(statement)
    return result.scalar()


async def check_user_exists(db: AsyncSession, user: UserSignin):
    db_user = await get_db_user(db, user.name)
    if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or passowrd")


async def check_user_duplicate(db: AsyncSession, user: UserCreate):
    user_by_name = await get_db_user(db, user.name)
    user_by_email = await get_db_user(db, user.user_email)
    if user_by_name or user_by_email:
        raise HTTPException(status_code=400, detail="username or email already exits")


async def get_user(db: AsyncSession, email: str) -> User:
    statement = select(User).where(User.email == email)
    result = await db.execute(statement)
    return result.scalar()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    await check_user_duplicate(db, user)
    password_hash = pwd_context.hash(user.password)
    db_user = User(name=user.name, password_hash=password_hash, email=user.user_email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user: UpdateUser) -> User:
    statement = (
        select(User).where(User.name == user.name).where(User.email == user.user_email)
    )
    result = await db.execute(statement)
    db_user = result.scalar()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or email")
    hashed_password = pwd_context.hash(user.password)
    db_user.password_hash = hashed_password
    await db.commit()
    return db_user


async def delete_user(db: AsyncSession, user_id: int) -> None:
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()
