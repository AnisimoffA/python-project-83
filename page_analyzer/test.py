from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor
import os
import psycopg2


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

try:
    connection = psycopg2.connect(DATABASE_URL)
    connection.autocommit = True

    with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            '''SELECT id FROM urls WHERE name = %s;''', ('http://stub.com',)
        )
        
        answer = cursor.fetchone().id
        print(answer)

except Exception:
    print("ОШИБКА")
    


