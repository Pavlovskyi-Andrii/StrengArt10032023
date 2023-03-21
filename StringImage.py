import numpy as np
import os
from PIL import ImageDraw
from PIL import ImageFont
import random
from tqdm import tqdm
import sqlite3
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import io





def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, 'wb') as file:
        file.write(data)
    print("Данные из blob сохранены в: ", filename, "\n")

def read_blob_data():
    try:
        sqlite_connection = sqlite3.connect('stringart.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_fetch_blob_query = """SELECT * from stringart"""
        cursor.execute(sql_fetch_blob_query)
        records = cursor.fetchall()
        for row in records:
            print("Id = ", row[0], "image_data = ")
            id = row[0]
            image_data  = row[1]

            print("Сохранение изображения  \n")
            photo_path = os.path.join(f"db_data+{id}" +".png")

            write_to_file(image_data, photo_path)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

read_blob_data()









# # Имя файла базы данных
# db_filename = 'stringart.db'
#
# # Папка, в которую будут сохранены изображения
# image_folder = 'image'
#
# # Подключение к базе данных
# connection = sqlite3.connect(db_filename)
#
# # Получение курсора
# cursor = connection.cursor()
#
# # Получение всех данных из таблицы stringart
# cursor.execute('SELECT * FROM stringart')
#
# # Извлечение всех строк с данными
# for row in cursor.fetchall():
#     # Получение id изображения
#     image_id = row[0]
#
#     # Получение бинарных данных изображения
#     image_data = row[1]
#
#     # Создание объекта изображения
#     image = Image.frombytes('RGB', (300, 300), image_data)
#
#     # Создание папки, если она не существует
#     if not os.path.exists(image_folder):
#         os.makedirs(image_folder)
#
#     # Сохранение изображения в файл
#     image.save(os.path.join(image_folder, f'{image_id}.jpg'))
#
# # Закрытие соединения с базой данных
# connection.close()





#
#
# # Название базы данных
# database_name = 'stringart.db'
#
# # Путь к папке для сохранения фото
# photo_folder_path = './photos'
#
# # Проверяем, существует ли папка для сохранения фото, если нет - создаем ее
# if not os.path.exists(photo_folder_path):
#     os.makedirs(photo_folder_path)
#
# # Создаем соединение с базой данных
# conn = sqlite3.connect(database_name)
#
# # Создаем курсор
# cursor = conn.cursor()
#
# # Выбираем данные из таблицы stringart с id = 1
# cursor.execute("SELECT image_data FROM stringart WHERE id = 1")
#
# # Получаем данные из ячейки Blob
# image_data = cursor.fetchone()[0]
#
# # Создаем новый файл в папке photos и записываем в него данные из ячейки Blob
# with open(os.path.join(photo_folder_path, 'image.jpg'), 'wb') as f:
#     f.write(image_data)
#
# # Закрываем курсор и соединение с базой данных
# cursor.close()
# conn.close()






# Класс имеет следующие методы:
# __init__: инициализирует объект класса, принимая в качестве параметров
# img_data - данные изображения в бинарном формате, radius - радиус круга,
# nPins - количество креплений, используемых для создания изображения.
# PrepareImage: метод, который подготавливает изображение для работы алгоритма.

class StringImageCircle():
    global img_data, radius, nPins

    def __init__(self, img_data, radius, nPins):
        self.img, self.img_res = self.PrepareImage(img_data, radius)
        self.radius = radius
        self.nPins = nPins

# PrepareImage: метод, который подготавливает изображение для работы алгоритма.
# Принимает img_data - данные изображения в бинарном формате и radius - радиус круга.
# Метод обрезает и изменяет размер изображения, удаляет фон, который не является
# частью изображения, и создает копию
#  изображения для использования в дальнейшем.
    def PrepareImage(self, img_data, radius):
        # Если img_data является путем к файлу
        if isinstance(img_data, str):
            with open(img_data, 'rb') as f:
                im_t = Image.open(f).convert('L')
        # Если img_data является данными в бинарном формате
        else:
            im_t = Image.open(io.BytesIO(img_data)).convert('L')

        w, h = im_t.size
        min_dim = min(h, w)
        top = int((h - min_dim) / 2)
        left = int((w - min_dim) / 2)
        im_croped = im_t.crop((left, top, left + min_dim, top + min_dim)).resize((radius * 2 + 1, radius * 2 + 1))
        img = np.asarray(im_croped).copy()
        y, x = np.ogrid[-radius:radius + 1, -radius:radius + 1]
        mask = x ** 2 + y ** 2 > radius ** 2
        img[mask] = 255
        img = 255 - img  # negative image

        img_res = np.ones(img.shape) * 255
        print(" PrepareImage подготовка фото")
        return img, img_res

        # PreparePins: метод, который подготавливает крепления для работы алгоритма.
        # Принимает radius - радиус круга и nPins - количество креплений. Метод создает
        #  массив точек для каждого крепления вокруг центра круга,
        #  с добавлением случайного шума для уменьшения эффекта муара.
    def PreparePins(self, radius, nPins):

        alpha = np.linspace(0, 2 * np.pi, nPins + 1)
        PinPos = []
        for angle in alpha[0:-1]:
            x = int(radius + radius * np.cos(angle))
            y = int(radius + radius * np.sin(angle))
            # adding noise to Pin Positions in order to reduce Moire effect
            if x > 5:
                x = x - random.randint(0, 5)
            elif x < (2 * radius - 5):
                x = x + random.randint(0, 5)
            if y > 5:
                y = y - random.randint(0, 5)
            elif y < (2 * radius - 5):
                y = y - random.randint(0, 5)
            PinPos.append((x, y))
        print(" PreparePins Обработка фото 2")
        return PinPos

    def getLineMask(self, pin1, pin2):
        length = int(np.hypot(pin2[0] - pin1[0], pin2[1] - pin1[1]))
        x = np.linspace(pin1[0], pin2[0], length)
        y = np.linspace(pin1[1], pin2[1], length)
        return (x.astype(int) - 1, y.astype(int) - 1)

    def LineScore(self, line):
        score = np.sum(line)
        score = score / (line.shape[0] + 0.001)  # add 0.001 to avoid divide by 0 error
        # penalty = sum(line<=10)
        # score = 0.6*score + 0.4*penalty
        score_mean = np.mean(line) if len(line) > 0 else 0
        return score, score_mean

    def FindBestNextPin(self, currentPin):
        bestScore = -999999
        bestPin = -1
        bestMean = 0
        for p in range(self.nPins - 1):
            nextPin = (p + currentPin) % self.nPins
            if abs(currentPin - nextPin) < 10: continue
            if (currentPin, nextPin) in self.Lines: continue
            tx, ty = self.getLineMask(self.PinPos[currentPin], self.PinPos[nextPin])
            tempLine = self.img[tx, ty]
            tempScore, tempMean = self.LineScore(tempLine)
            if tempScore > bestScore:
                bestScore = tempScore
                bestPin = nextPin
                bestMean = tempMean
        print("обработка пин")
        return bestPin, bestMean

    def SaveImage(self, image_matrix, file_path, description, color=(255, 0, 0), position=(10, 10)):
        imtemp = Image.fromarray(image_matrix).convert('RGB')
        drawer = ImageDraw.Draw(imtemp)
        print("сохранение фото")
        font = ImageFont.truetype("font.ttf", 36)

        drawer.text(position, description, color, font=font)
        imtemp.save(file_path)

    def Convert(self, max_lines=2000):
        currentPin = random.randint(0, self.nPins)
        for l in tqdm(range(max_lines)):
            bestPin, bestMean = self.FindBestNextPin(currentPin)
            self.Lines.append((currentPin, bestPin))
            tx, ty = self.getLineMask(self.PinPos[currentPin], self.PinPos[bestPin])
            self.img[tx, ty] = np.maximum(self.img[tx, ty] - bestMean, 0)
            self.img_res[tx, ty] = np.maximum(self.img_res[tx, ty] - bestMean, 0)
            currentPin = bestPin
        return self.img_res


class StringImageSquare:
    global img_data, nPins
    def __init__(self, img_data, dimension, nPins, noise=5):
        self.dimension = dimension
        self.nPins = nPins
        self.noise = noise
        self.img, self.img_res = self.PrepareImage(img_data, dimension)
        self.PinPos = self.PreparePins(dimension)
        self.Lines = []


    def PrepareImage(self, img_data, dimension):

        if isinstance(img_data, str):
            with open(img_data, 'rb') as f:
                im_t = Image.open(f).convert('L')
        # Если img_data является данными в бинарном формате
        else:
            im_t = Image.open(io.BytesIO(img_data)).convert('L')

        w, h = im_t.size
        min_dim = min(h, w)
        top = int((h - min_dim) / 2)
        left = int((w - min_dim) / 2)
        im_croped = im_t.crop((left, top, left + min_dim, top + min_dim)).resize((dimension + 1, dimension + 1))
        img = np.asarray(im_croped).copy()
        img = 255 - img
        img_res = np.ones(img.shape) * 255
        print("отримане фото")
        return img, img_res

    def PreparePins(self, dimension):
        if (self.nPins % 4) != 0:
            self.nPins = self.nPins + (self.nPins % 4)

        PinPos = []
        step_size = int(dimension // (self.nPins / 4))
        # locate pins on square surface in clock-wise basis
        for i in range(0, dimension, step_size):
            PinPos.append((0, i))  # (0,0) -> (0,d)
        for i in range(0, dimension, step_size):
            PinPos.append((i, dimension))  # (0,d) -> (d,d)
        for i in range(dimension, 0, -step_size):
            PinPos.append((dimension, i))  # (d,d) -> (d,0)
        for i in range(dimension, 0, -step_size):
            PinPos.append((i, 0))  # (d,0) -> (0,0)

        # Remove duplicate pins in corners
        PinPos = list(dict.fromkeys(PinPos))

        # Add Noise
        noisy_pins = []
        for p in PinPos:
            x = p[0]
            y = p[1]
            if x >= dimension:
                x = x - random.randint(0, self.noise)
            else:
                x = x + random.randint(0, self.noise)
            if y >= dimension:
                y = y - random.randint(0, self.noise)
            else:
                y = y + random.randint(0, self.noise)
            noisy_pins.append((x, y))
        self.nPins = len(noisy_pins)
        return noisy_pins

    def DrawPins(self):
        for p in self.PinPos:
            self.img[p[0], p[1]] = 0
        return self.img

    def getLineMask(self, pin1, pin2):
        length = int(np.hypot(pin2[0] - pin1[0], pin2[1] - pin1[1]))
        x = np.linspace(pin1[0], pin2[0], length)
        y = np.linspace(pin1[1], pin2[1], length)
        return (x.astype(int) - 1, y.astype(int) - 1)

    def LineScore(self, line):
        score = np.sum(line)
        score = score / (line.shape[0] + 0.001)
        # penalty = sum(line <= 10)
        # score = 0.6*score + 0.4*penalty
        score_mean = np.mean(line) if len(line) > 0 else 0
        return score, score_mean

    def FindBestNextPin(self, currentPin):
        bestScore = -999999
        bestPin = -1
        bestMean = 0
        for p in range(self.nPins - 1):
            nextPin = (p + currentPin) % self.nPins
            if abs(currentPin - nextPin) < 10: continue
            if (currentPin, nextPin) in self.Lines: continue
            tx, ty = self.getLineMask(self.PinPos[currentPin], self.PinPos[nextPin])
            tempLine = self.img[tx, ty]
            tempScore, tempMean = self.LineScore(tempLine)
            if tempScore > bestScore:
                bestScore = tempScore
                bestPin = nextPin
                bestMean = tempMean
        return bestPin, bestMean

    def SaveImage(self, image_matrix, file_path, description, color=(255, 0, 0), position=(10, 10)):
        imtemp = Image.fromarray(image_matrix).convert('RGB')
        drawer = ImageDraw.Draw(imtemp)
        font = ImageFont.truetype("font.ttf", 36)
        drawer.text(position, description, color, font=font)
        imtemp.save(file_path)

    def Convert(self, max_lines=2000):
        currentPin = random.randint(0, self.nPins)
        for l in tqdm(range(max_lines)):
            bestPin, bestMean = self.FindBestNextPin(currentPin)
            self.Lines.append((currentPin, bestPin))
            tx, ty = self.getLineMask(self.PinPos[currentPin], self.PinPos[bestPin])
            self.img[tx, ty] = np.maximum(self.img[tx, ty] - bestMean, 0)
            self.img_res[tx, ty] = np.maximum(self.img_res[tx, ty] - bestMean, 0)
            currentPin = bestPin
        f_img = Image.fromarray(self.img_res).convert('RGB')
        f_img.save('result.jpg')
        return self.img_res


def extract_images_from_database():
    conn = sqlite3.connect('stringart.db')
    cursor = conn.cursor()
    cursor.execute('SELECT image_data FROM stringart')
    results = cursor.fetchall()
    conn.close()

    html = '<html><body>'
    for row in results:
        img_data = row[0]
        im_t = Image.open(BytesIO(img_data))
        html += '<img src="data:image/png;base64,{0}">'.format(im_t)
    html += '</body></html>'
    with open('result.html', 'w') as f:
        f.write(html)



# c = StringImageCircle("112.png",200 , 200 )  # ok
# c.PrepareImage("112.png",200) # ok
# c.PreparePins(200,200)   # ok
#
# with open('112.png', 'rb') as img_file:
#
#     img_data = img_file.read()
#
# f = StringImageSquare(img_data, 400, 200, noise=5)
# #f.PrepareImage(f,400)
# img_data_bytes = f.img_res.tobytes()
# f.PrepareImage(img_data_bytes, 400)






# class StringImageSquare:
#     global img_data, nPins
#     def __init__(self, img_data, dimension, nPins, noise=5):

def readSqliteTable():
    conn = sqlite3.connect('stringart.db')
    cursor = conn.cursor()

    cursor.execute('SELECT image_data, nLines, nPins, radius FROM stringart')
    row = cursor.fetchone()
    img_data, nLines, nPins, radius = row
    print(f"Виводить данние "
          f"Количество линий: {nLines},"
          f"Количество понов: {nPins},"
          f"Радиус круга: {radius} ")


    # print(img_data)
    return img_data, nLines, nPins, radius

img_data, nLines, nPins, radius = readSqliteTable()


string_circle = StringImageCircle(img_data, radius, nPins)
plt.imshow(string_circle.img_res, cmap='gray')
plt.show()





















#
#
# string_square = StringImageSquare(img_data, radius, nPins)
# plt.imshow(string_square.img_res, cmap='gray')
# plt.show()

# if __name__ == '__main__':
#     converter = StringImageCircle(img_data, radius, nPins)
#     img_res = converter.Convert(max_lines=nLines)
#     plt.imshow(img_res, cmap='gray')
#     plt.show()





#Сюда подставляем данные

#
# def readSqliteTable():
#     global img_data, nLines, nPins, radius
#     try:
#         sqliteConnection = sqlite3.connect('stringart.db')
#         cursor = sqliteConnection.cursor()
#         print("Connected to SQLite")
#
#         sqlite_select_query = """SELECT * from stringart"""
#         cursor.execute(sqlite_select_query)
#         records = cursor.fetchall()
#         print("Total rows are:  ", len(records))
#         print("Printing each row")
#         for row in records:
#             print("Id: ", row[0])
#             img_path  = row[1]
#             img_data = Image.open(BytesIO(img_path))
#             nLines = row[2]
#             nPins = row[3]
#             radius = row[4]
#
#             # Создайте экземпляр StringImageCircle со значениями из базы данных
#             string_circle = StringImageCircle(img_data, radius, nPins)
#
#             # Сделайте что-нибудь с экземпляром StringImageCircle здесь
#             # пример вывода
#             string_circle.img.show()
#             print(f"Радиус: {string_circle.radius}, Количестов гвоздиков : {string_circle.nPins}")
#
#             print("\n")
#
#         cursor.close()
#
#     except sqlite3.Error as error:
#         print("Failed to read data from sqlite table", error)
#         sqliteConnection.close()
#     finally:
#         if sqliteConnection:
#             sqliteConnection.close()
#             print("The SQLite connection is closed")
#
#     return img_data, nLines, nPins, radius
#
# # визов функций чтоб получить значение переменни
# img_data, nLines, nPins, radius = readSqliteTable()
#
# # Now you can use the variables in other parts of your code
#
#
#
# if __name__ == '__main__':
#     converter = StringImageCircle(img_data, radius, nPins)
#     converter.img.show()
#     #______________Добавлен из оригинал
#     img_res = converter.Convert(max_lines=nLines)
#     plt.imshow(img_res, cmap='gray')
#     plt.show()




# if __name__ == '__main__':
# img_res = converter.Convert(max_lines=nLines)
#     plt.imshow(img_res, cmap='gray')
#     plt.show()




# img_path = 'photos/image.jpg'
# if not os.path.exists(img_path):
#     raise FileNotFoundError(f'Image not found at {img_path}')
# string_circle = StringImageCircle(img_path, radius, nPins)




# img_path =None            # "/photos/image.png"
# nLines = None
# nPins = None
# radius = None
#img_path = "/photos/image.png"
# radius = 500
# nPins = 300
# nLines = 2000

# Usage
# if __name__ == '__main__':
#     # global img_path, radius, nPins, nLines
#     # converter = StringImageCircle(img_path, radius, nPins)
#     string_circle = StringImageCircle(img_data, radius, nPins)
#     img_res = converter.Convert(max_lines=nLines)
#     plt.imshow(img_res, cmap='gray')
#     plt.show()





