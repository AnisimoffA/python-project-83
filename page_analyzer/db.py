from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor
import psycopg2
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def insert_into_db(requirement, values):
    try:
        connection = connect_db()
        connection.autocommit = True

        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(requirement, values)

    except Exception as Ex:
        print('[INFO]Ошибка: ', Ex)
    finally:
        if connection:
            connection.close()
            print('[INFO]Соединение закрыто')


def select_one_from_db(requirement, values):
    try:
        connection = connect_db()
        connection.autocommit = True

        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(requirement, values)

            data = cursor.fetchone()

    except Exception as Ex:
        print('[INFO]Ошибка: ', Ex)
    finally:
        if connection:
            connection.close()
            print('[INFO]Соединение закрыто')
            return data


def select_many_from_db(requirement, values):
    try:
        connection = connect_db()
        connection.autocommit = True

        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(requirement, values)

            data = cursor.fetchall()

    except Exception as Ex:
        print('[INFO]Ошибка: ', Ex)
    finally:
        if connection:
            connection.close()
            print('[INFO]Соединение закрыто')
            return data
