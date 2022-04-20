from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLACHEMY_DATABASE_URL = settings.DATABASE_URL.replace("://", "ql://", 1)


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


