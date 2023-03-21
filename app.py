import sqlite3
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URL']='sqlite3:///stringart.db'



# Создание таблицы в базе данных, если она еще не существует
def create_table():
    conn = sqlite3.connect('stringart.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stringart
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, image_data BLOB, radius INTEGER, nPins INTEGER, nLines INTEGER)''')
    conn.commit()
    conn.close()


# функция для получения пути к фотографии по ее номеру
def get_photo_path(id):
    return os.path.join("db_data" + str(id) + ".png")

@app.route("/")
def index():
    try:
        # установление соединения с базой данных
        conn = sqlite3.connect('stringart.db')
        c = conn.cursor()

        # выборка всех строк из таблицы
        c.execute("SELECT * FROM stringart")

        # получение результатов запроса
        rows = c.fetchall()

        # закрытие соединения с базой данных
        conn.close()

        # формирование списка с путями к фотографиям
        photos = [get_photo_path(row[0]) for row in rows]

        # рендеринг шаблона и передача списка фотографий в контекст
        return render_template("index.html", photos=photos)

    except Exception as e:
        return str(e)

# Функция для сохранения данных из формы в базу данных
def save_to_db(image_data, radius, nPins, nLines):
    conn = sqlite3.connect('stringart.db')
    c = conn.cursor()
    c.execute('''INSERT INTO stringart (image_data, radius, nPins, nLines) VALUES (?, ?, ?, ?)''', (image_data, radius, nPins, nLines))
    conn.commit()
    conn.close()

# обработчик POST запроса для формы
@app.route('/submit_form', methods=['POST'])
def submit_form():
    # получение данных из формы
    image_data = request.form['image_data']
    radius = request.form['radius']
    nPins = request.form['nPins']
    nLines = request.form['nLines']

    # сохранение данных в базу данных
    save_to_db(image_data, radius, nPins, nLines)

    # перенаправление на главную страницу
    return redirect("/")



@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/thank')
def thank():
    return render_template('thank.html')








#Маршрут для обработки формы
@app.route('/generate', methods=['POST'])
def generate():
    # Получение данных из формы
    image_data = request.files['image_data'].read()
    radius = request.form['radius']
    nPins = request.form['nPins']
    nLines = request.form['nLines']

    # Сохранение данных в базу данных
    save_to_db(image_data, radius, nPins, nLines)

    # Возвращение сообщения об успешном сохранении

    return render_template('generate.html')




if __name__ == '__main__':
    app.run(debug=True)


# Маршрут для отображения формы












