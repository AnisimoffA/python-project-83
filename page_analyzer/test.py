# from dotenv import load_dotenv
# from psycopg2.extras import NamedTupleCursor
# import os
# import psycopg2


# load_dotenv()
# DATABASE_URL = os.getenv('DATABASE_URL')
# SECRET_KEY = os.getenv('SECRET_KEY')

# try:
#     connection = psycopg2.connect(DATABASE_URL)
#     connection.autocommit = True

#     with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
#         cursor.execute(
#             '''SELECT id FROM urls ORDER BY id DESC LIMIT 1;'''
#         )
        
#         answer = cursor.fetchone().id
#         print(answer)

# except Exception:
#     print("ОШИБКА")


#[Record(id=20, name='https://www.google.com', created_at=None, status_code=None), 
# Record(id=17, name='https://www.avito.ru', created_at=None, status_code=None), 
# Record(id=16, name='https://ru.tradingview.com', created_at=None, status_code=None), 
# Record(id=15, name='https://railway.app', created_at=datetime.date(2023, 7, 22), status_code=200), 
# Record(id=14, name='https://www.db-fiddle.com', created_at=datetime.date(2023, 7, 22), status_code=200), 
# Record(id=13, name='https://cars.av.by', created_at=datetime.date(2023, 7, 22), status_code=200), 
# Record(id=12, name='https://ru.hexlet.io', created_at=datetime.date(2023, 7, 22), status_code=200)

print("" == None)