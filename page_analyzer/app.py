from flask import Flask, render_template, request, redirect, url_for, session, flash # NOQA E501
from datetime import date
from page_analyzer.validator import url_validator, url_normalize
import psycopg2
import os
import requests
from page_analyzer.url_analyzer import url_analyze
from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


def connect_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/urls')
def list_page():
    try:
        connection = connect_db()
        connection.autocommit = True

        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                '''SELECT DISTINCT ON (urls.id) urls.id, name,
                url_checks.created_at, status_code FROM urls
                LEFT JOIN url_checks ON urls.id = url_checks.id
                ORDER BY id DESC;'''
            )

            data = cursor.fetchall()

    except Exception as Ex:
        print('[INFO]Ошибка: ', Ex)
    finally:
        if connection:
            connection.close()
            print('[INFO]Соединение закрыто')
    return render_template('list_of_urls.html', data=data)


@app.post('/urls')
def post_urls():
    URL = request.form['url']

    if not url_validator(URL):
        flash('Некорректный URL', category="danger")
        return render_template("index.html"), 422

    URL = url_normalize(URL)
    try:
        connection = connect_db()
        connection.autocommit = True
        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor: # NOQA E501
            cursor.execute(
                '''SELECT id FROM urls WHERE name = %s;''', (URL,)
            )
            id = cursor.fetchone()
            if id:
                flash('Страница уже существует', 'info')
                return redirect(url_for('link_page', id=id.id))

        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor: # NOQA E501
            cursor.execute(
                '''INSERT INTO urls (name, created_at)
                VALUES (%s, %s);''',
                (URL, date.today())
            )
            print('[INFO]Запись добавлена')

        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor: # NOQA E501
            cursor.execute(
                '''SELECT id FROM urls ORDER BY id DESC LIMIT 1;'''
            )

            id = cursor.fetchone().id

        flash('Страница успешно добавлена', 'success') # NOQA E501
        return redirect(url_for('link_page', id=id))

    except Exception as Ex:
        print('[INFO]Ошибка: ', Ex)
    finally:
        if connection:
            connection.close()
            print('[INFO]Соединени закрыто')


@app.route('/urls/<id>')
def link_page(id):
    try:
        connection = connect_db()
        connection.autocommit = True

        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                '''SELECT * FROM urls WHERE id = %s;''', (id,)
            )
            data_about_url = cursor.fetchall() # NOQA E501

            cursor.execute(
                '''SELECT id, status_code, h1, title, description,
                created_at FROM url_checks WHERE url_id = %s
                ORDER BY id DESC;''', (id,)
            )
            data = cursor.fetchall()
            print('[INFO]Данные выбраны')

            return render_template('link_page.html',
                                   data_about_url=data_about_url,
                                   id=id,
                                   data=data)

    except Exception as Ex:
        print('[INFO]Ошибка: ', Ex)
    finally:
        if connection:
            connection.close()
            print('[INFO]Соединение закрыто')


@app.post('/urls/<id>/check')
def url_check(id):
    try:
        connection = connect_db()
        connection.autocommit = True

        with connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                        '''SELECT name FROM urls WHERE id = %s;''', (id,) # NOQA E501
            )

            name = cursor.fetchone().name
            request = requests.get(name)
            if request.status_code == 200:
                flash('Страница успешно проверена', 'success') # NOQA E501
                status_code, h1, title, description = url_analyze(name)
                cursor.execute(
                    '''INSERT INTO url_checks (url_id,
                    status_code, h1, title, description,
                    created_at) VALUES (%s, %s, %s, %s, %s, %s)''',
                    (id, status_code, h1, title, description, date.today())
                )
            else:
                flash('Произошла ошибка при проверке', 'danger') # NOQA E501
                redirect(url_for('link_page', id=id))

    except Exception as Ex:
        flash('Произошла ошибка при проверке', 'danger')
        print('[INFO]Ошибка: ', Ex)
        redirect(url_for('link_page', id=id))
    finally:
        if connection:
            connection.close()
            print('[INFO]Соединение закрыто')

    return redirect(url_for('link_page', id=id))


@app.errorhandler(404)
def error_page(e):
    return render_template("error_page.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
