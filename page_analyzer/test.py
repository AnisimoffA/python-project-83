from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

def connect_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

print(DATABASE_URL)
connect_db()