from app.models.base import User
from app.schemas import UpdateUser
from app.schemas import UserCreate
from app.schemas import UserLogin
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_user_exists(db: Session, user: UserLogin):
    db_user = db.query(User).filter(User.name == user.name).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or passowrd")


def check_user_duplicate(db: Session, email: str):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="eamil already exists")


def get_user(db: Session, user_id: int) -> User:
    check_user_exists(db, user_id)
    db_user = db_user = db.query(User).filter(User.id == user_id).first()
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


async def create_user(db: Session, user: UserCreate) -> User:
    check_user_duplicate(db, user.user_email)
    password_hash = pwd_context.hash(user.password)
    db_user = User(name=user.name, password_hash=password_hash, email=user.user_email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: UpdateUser) -> User:
    check_user_exists(db, user_id)
    db_user = db.query(User).filter(User.id == user_id).first()
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.commit()
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    check_user_exists(db, user_id)
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
