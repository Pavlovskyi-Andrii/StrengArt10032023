

import sqlite3
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy



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

# Функция для сохранения данных из формы в базу данных
def save_to_db(image_data, radius, nPins, nLines):
    conn = sqlite3.connect('stringart.db')
    c = conn.cursor()
    c.execute('''INSERT INTO stringart (image_data, radius, nPins, nLines) VALUES (?, ?, ?, ?)''', (image_data, radius, nPins, nLines))
    conn.commit()
    conn.close()

# Маршрут для отображения формы
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для обработки формы


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
    return 'Данные сохранены в базе данных!'
    return render_template()

if __name__ == '__main__':
    create_table()
    app.run(debug=True)












class MyTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_data = db.Column(db.String(255))
    radius = db.Column(db.Integer)
    nPins = db.Column(db.Integer)
    nLines = db.Column(db.Integer)


"""
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    # получаем данные из формы
    image_data = request.files['image_data'].read()
    radius = request.form['radius']
    nPins = request.form['nPins']
    nLines = request.form['nLines']

    # сохраняем данные в базу данных
    conn = sqlite3.connect('streng1_DB.sl3')
    c = conn.cursor()
    c.execute('INSERT INTO images (image_data, radius, nPins, nLines) VALUES (?, ?, ?, ?)',
              (image_data, radius, nPins, nLines))
    conn.commit()
    conn.close()

    # отправляем пользователю сообщение об успешной генерации
    return 'Image generated successfully!'


if __name__ == '__main__':
    app.run(debug=True)

"""











# from flask import Flask, request
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"]="streng1_DB.db"
# db = SQLAlchemy(app)
#
#
# @app.route("/")
#
#
#
# class Image(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     image_data = db.Column(db.LargeBinary)
#     radius = db.Column(db.integer.request.form['radius'])
#     nPins = int(request.form['nPins'])
#     nLines = int(request.form['nLines'])
#
#     def __repr__(self):  # указіваем какое значение возвращаем с базы данных
#         return "<Contact %r>" % self.id
#
#
#
#
#
# def upload_image("/", methods=["POST","GET"]):
#     if request.method == "POST":
#
#         image_file = request.files['image']
#         image_data = image_file.read()
#         new_image = Image(image_data=image_data)
#         radius = request.form["radius"]
#         nPins = request.form["nPins"]
#         nLines = request.form["nLines"]
#
#         image = Image(image_file=image_file, radius=radius, nPins=nPins, nLines=nLines)
#
#
#         try:
#             db.session.add(new_image)
#             db.session.commit()
#     else:
#
#
#         return 'Image uploaded successfully'
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True)





