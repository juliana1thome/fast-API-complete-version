from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLACHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_passw}@{settings.db_hostname}/{settings.db_name}'


# The engine is responsable for sqlalchemy to connect to postgresql
engine = create_engine(SQLACHEMY_DATABASE_URL)

# When you want to talk to the database you need a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All the models defined that create the tables in postgresql will be expending this base class ↓
Base = declarative_base()

# Create dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


