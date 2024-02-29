import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# database engine
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# session
session = sessionmaker(bind=engine)


# database connection
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
