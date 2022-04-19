import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

class Connect():
    while True:
        try:
            # Connect to an existing database
            conn = psycopg2.connect(host = settings.DB_HOSTNAME, database = settings.DB_NAME, user = settings.DB_USERNAME, password = settings.DB_PASSW, cursor_factory = RealDictCursor)

            # Open a cursor to perform database operations
            cursor = conn.cursor()
            print("Database Connection was Succesfull!!")
            break

        except Exception as error:
            print("Connecting to database failed")
            print("Error: ", error)
            time.sleep(5)


connect = Connect()
