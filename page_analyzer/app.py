from flask import Flask, render_template, request, redirect, url_for, session, flash # NOQA E501
from datetime import date
from page_analyzer.validator import url_validator, url_normalize
import psycopg2
import os
import requests
from page_analyzer.url_analyzer import url_analyze
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
# ----------------database info opened------------------


def connect_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


@app.route('/', methods=['POST', 'GET'])
def main_page():
    session.clear()

    if request.method == "POST":
        URL = request.form['url']
        if url_validator(URL):
            URL = url_normalize(URL)
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
                        '''SELECT id FROM urls ORDER BY id DESC LIMIT 1;'''
                    )

                    id = cursor.fetchone()[0] # NOQA E501
                    print("id ---------------", id)
                    print('[INFO]Данные выбраны')

                session['flash_message'] = ('Страница успешно добавлена', 'success') # NOQA E501
                parsed_url = url_normalize(URL) # NOQA 
                return redirect(url_for('link_page', id=id))

            except Exception:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f'''SELECT id FROM urls WHERE name = '{URL}';'''
                    )
                    session['flash_message'] = ('Страница уже существует', 'info') # NOQA E501
                    id = cursor.fetchone()[0]
                    return redirect(url_for('link_page', id=id)) # NOQA E501

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
                '''SELECT DISTINCT ON (urls.id) urls.id, name, url_checks.created_at, status_code FROM urls LEFT JOIN url_checks ON urls.id = url_checks.id ORDER BY id DESC;'''
            )

            data = cursor.fetchall()
            print(data)

    except Exception as Ex:
        print('[INFO]Ошибка: ', Ex)
    finally:
        if connection:
            connection.close()
            print('[INFO]Соединение закрыто')
    return render_template('list_of_urls.html', data=data)


@app.route('/urls/<id>')
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
            data_about_url = cursor.fetchall() # NOQA E501

        with connection.cursor() as cursor:
            cursor.execute(
                f'''SELECT id, status_code, h1, title, description, created_at FROM url_checks WHERE url_id = '{id}';'''
            )
            data = cursor.fetchall()

            print('[INFO]Данные выбраны')

    except Exception as Ex:
        print('[INFO]Ошибка: ', Ex)
    finally:
        if connection:
            connection.close()
            print('[INFO]Соединение закрыто')

    return render_template('link_page.html',
                           data_about_url=data_about_url,
                           id=id,
                           data=data)


@app.post('/urls/<id>/check')
def url_check(id):
    try:
        connection = connect_db()
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                        f'''SELECT name FROM urls WHERE id = '{id}';''' # NOQA E501
            )
            
            name = cursor.fetchone()[0]
            request = requests.get(name)
            if request.status_code == 200:
                session['flash_message'] = ('Страница успешно проверена', 'success')
                status_code, h1, title, description = url_analyze(name)
                cursor.execute(
                        f'''INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES ('{id}', '{status_code}', '{h1}', '{title}', '{description}', '{date.today()}');''' # NOQA E501
                )
            else:
                session['flash_message'] = ('Произошла ошибка при проверке', 'danger')

    except Exception as Ex:
        session['flash_message'] = ('Произошла ошибка при проверке', 'danger')
        print('[INFO]Ошибка: ', Ex)
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
