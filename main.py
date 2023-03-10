from flask import Flask, render_template, request, redirect
from StringImage import StringImageCircle
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from matplotlib import pyplot as plt
import random
from tqdm import tqdm
import os



import sqlite3
#конект к streng1_DB.sl3 ктоторий ми создали


connection = sqlite3.connect('streng1_DB.sl3',5)
cur=connection.cursor()

#cur.execute('CREATE TABLE first_art (name TEXT);')
cur.execute("INSERT INTO first_art (name) VALUES ('NICK');")

connection.commit()
connection.close()



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Получаем параметры из POST-запроса
    radius = int(request.form['radius'])
    nPins = int(request.form['nPins'])
    nLines = int(request.form['nLines'])
    # Сохраняем загруженное изображение на диск
    file = request.files['image']
    filename = file.filename
    file.save(os.path.join('uploads', filename))
    # Генерируем изображение в стиле string art
    string_image = StringImageCircle(os.path.join('uploads', filename), radius, nPins)
    string_image.Convert(max_lines=nLines)
    # Сохраняем сгенерированное изображение на диск
    result_filename = os.path.join('static', 'result.png')
    string_image.SaveImage(string_image.img_res, result_filename, 'Result')
    # Возвращаем страницу с результатом
    return render_template('result.html')





if __name__ == '__main__':
    app.run(debug=True)


