from typing import Optional

from models import User
from sqlalchemy.orm import Session
from schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    password_hash = pwd_context.hash(user.password)
    db_user = User(name=user.name, password_hash=password_hash, email=user.user_email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: User) -> Optional[User]:
    db_user = db.query(User).filter(User.id == user_id).first()
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    return db_user


def delete_user(db: Session, user_id: int) -> None:
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
