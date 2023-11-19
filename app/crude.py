from model import User
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, user: User):
    db_user = db.query(User).filter(User.id == user_id).first()
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    return db_user


def delete_user(db: Session, user_id: int):
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
