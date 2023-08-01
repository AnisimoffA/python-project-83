from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor
import psycopg2
from psycopg2 import pool # NOQA F401
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
connect_db = psycopg2.pool.SimpleConnectionPool(1, 20, DATABASE_URL)


def insert_into_db(requirement, values):
    try:
        connection = connect_db.getconn()
        connection.autocommit = True

        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(requirement, values)

    except Exception as Ex:
        print('[INFO]Ошибка: ', Ex)
    finally:
        if connection:
            connect_db.putconn(connection)
            print('[INFO]Соединение закрыто')


def select_one_from_db(requirement, values):
    try:
        connection = connect_db.getconn()
        connection.autocommit = True

        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(requirement, values)

            data = cursor.fetchone()

    except Exception as Ex:
        print('[INFO]Ошибка: ', Ex)
    finally:
        if connection:
            connect_db.putconn(connection)
            print('[INFO]Соединение закрыто')
            return data


def select_many_from_db(requirement, values):
    try:
        connection = connect_db.getconn()
        connection.autocommit = True

        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(requirement, values)

            data = cursor.fetchall()

    except Exception as Ex:
        print('[INFO]Ошибка: ', Ex)
    finally:
        if connection:
            connect_db.putconn(connection)
            print('[INFO]Соединение закрыто')
            return data
