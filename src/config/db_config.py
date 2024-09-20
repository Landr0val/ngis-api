from dotenv import load_dotenv
from os import getenv
from psycopg2 import connect

load_dotenv()

def get_db_connection():
    host = getenv("HOST_URL")
    port = getenv("PORT")
    database = getenv("DATABASE")
    user = getenv("DB_USER")
    password = getenv("DB_PASSWORD")

    return connect(host=host, database=database, user=user, password=password)
