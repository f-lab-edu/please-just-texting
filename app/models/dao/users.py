from app.models.base import User
from app.schemas import DeleteModel
from app.schemas import UserCreate
from app.schemas import UserSignin
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import and_
from sqlalchemy import delete
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_db_user(db: AsyncSession, field: str) -> User | None:
    statement = select(User).where(or_(User.name == field, User.email == field))
    result = await db.execute(statement)
    return result.scalar()


async def check_user_exists(db: AsyncSession, user: UserSignin):
    db_user = await get_db_user(db, user.name)
    if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")


async def check_user_duplicate(db: AsyncSession, user: UserCreate):
    user_by_name = await get_db_user(db, user.name)
    user_by_email = await get_db_user(db, user.user_email)
    if user_by_name or user_by_email:
        raise HTTPException(status_code=400, detail="username or email already exits")


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    await check_user_duplicate(db, user)
    password_hash = pwd_context.hash(user.password)
    db_user = User(name=user.name, password_hash=password_hash, email=user.user_email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, name, email, new_password) -> None:
    statement = select(User).where(User.name == name).where(User.email == email)
    result = await db.execute(statement)
    db_user = result.scalar()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Invalid username or email")
    hashed_password = pwd_context.hash(new_password)
    db_user.password_hash = hashed_password
    await db.commit()


async def delete_user(db: AsyncSession, user: DeleteModel) -> None:
    statement = delete(User).where(
        and_(User.name == user.name, User.email == user.email)
    )
    user_signin = UserSignin(name=user.name, password=user.password)
    await check_user_exists(user=user_signin, db=db)
    await db.execute(statement)
    await db.commit()
