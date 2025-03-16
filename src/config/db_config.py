import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import os

load_dotenv()

connection_pool = psycopg2.pool.SimpleConnectionPool(
            1,
            20,
            host=os.getenv("HOST_URL"),
            port=os.getenv("PORT"),
            database=os.getenv("DATABASE"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
 
def get_db_connection():
    try:
        connection = connection_pool.getconn()
        print("Connection getted of pool")
        return connection
    
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None
    
def realease_db_connection(connection):
    if connection:
        connection_pool.putconn(connection)
        print("Connection released to pool")

def close_connection_pool():
    if connection_pool:
        connection_pool.closeall()
        print("Connection pool closed")