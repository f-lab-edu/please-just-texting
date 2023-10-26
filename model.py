from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Sequence
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
