from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Fixing URI heroku problem
uri = settings.DATABASE_URL
if uri.startswith("postgres://"):
    uri = uri.replace("://", "ql://", 1)

SQLACHEMY_DATABASE_URL = uri

# Creating an instance of a engine that is responsable for
# SQLAlchemy to connect to postgresql
engine = create_engine(SQLACHEMY_DATABASE_URL)

# Create a session in order to communicate with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This base class ↓ is extended by the app models
Base = declarative_base()


# Create dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
