from flask import Flask, render_template, request, redirect, url_for, session, flash # NOQA E501
from datetime import date
from page_analyzer.validator import url_validator, url_normalize
import psycopg2
import os


DATABASE_URL = os.getenv('DATABASE_URL')
# ----------------database info opened------------------


def connect_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


try:
    connection = connect_db()
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            '''CREATE TABLE urls (
                    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                    name varchar(255) UNIQUE,
                    created_at date);'''
        )
        print('[INFO]Запрос отработан')

except Exception as Ex:
    print('[INFO]Ошибка: ', Ex)
finally:
    if connection:
        connection.close()
        print('[INFO]Соединение закрыто')

# ----------------database info closed------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = '3G23G#$%VHH>&<.4U,83NKJ'


@app.route('/', methods=['POST', 'GET'])
def main_page():
    session.clear()

    if request.method == "POST":
        URL = request.form['url']
        if url_validator(URL):
            try:
                connection = connect_db()
                connection.autocommit = True

                with connection.cursor() as cursor:
                    cursor.execute(
                        f'''INSERT INTO urls (name, created_at) VALUES ('{URL}', '{date.today()}');''' # NOQA E501
                    )
                    print('[INFO]Запись добавлена')

                with connection.cursor() as cursor:
                    cursor.execute(
                        '''SELECT * FROM urls ORDER BY id DESC LIMIT 1;'''
                    )

                    session['url_id'], session['url_name'], session['url_date'] = cursor.fetchone() # NOQA E501
                    print('[INFO]Данные выбраны')

                session['flash_message'] = ('Страница успешно добавлена', 'success') # NOQA E501
                parsed_url = url_normalize(URL) # NOQA 
                return redirect(url_for('link_page', id=session['url_id']))

            except Exception:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f'''SELECT id FROM urls WHERE name = '{URL}';'''
                    )
                    session['flash_message'] = ('Страница уже существует', 'info') # NOQA E501
                    session['url_id'] = cursor.fetchone()[0]
                    return redirect(url_for('link_page', id=session['url_id'])) # NOQA E501

            finally:
                if connection:
                    connection.close()
                    print('[INFO]Соединени закрыто')

        else:
            flash('Некорректный URL', category="danger")
            return render_template('index.html')

    return render_template('index.html')


@app.route('/urls')
def list_page():
    try:
        connection = connect_db()
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT * FROM urls;'''
            )

            data = cursor.fetchall()

    except Exception as Ex:
        print('[INFO]Ошибка: ', Ex)
    finally:
        if connection:
            connection.close()
            print('[INFO]Соединение закрыто')
    return render_template('list_of_urls.html', data=data)


@app.route('/<id>')
def link_page(id):
    if session:
        flash(session['flash_message'][0], category=session['flash_message'][1])

    try:
        connection = connect_db()
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                f'''SELECT * FROM urls WHERE id = '{id}';'''
            )

            session['url_id'], session['url_name'], session['url_date'] = cursor.fetchone() # NOQA E501

            print('[INFO]Данные выбраны')
    except Exception as Ex:
        print('[INFO]Ошибка: ', Ex)
    finally:
        if connection:
            connection.close()
            print('[INFO]Соединение закрыто')

    return render_template('link_page.html',
                           url_id=session['url_id'],
                           url_name=session['url_name'],
                           url_date=session['url_date'])


if __name__ == "__main__":
    app.run(debug=True)
