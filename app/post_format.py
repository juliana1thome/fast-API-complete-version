from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# from typing import Optional

# Defining my schema
# This makes you have a easier time extracting the data. So, you can only do this to extract title
# new_post.title (check main.py file to understand where this new_post comes from)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Default True

while True:
    try:
        # Connect to an existing database
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = settings.MY_DB_PASSW, cursor_factory = RealDictCursor)

        # Open a cursor to perform database operations
        cursor = conn.cursor()
        print("Database Connection was Succesfull!!")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(5)

