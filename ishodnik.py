import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from matplotlib import pyplot as plt
import random
from tqdm import tqdm
import io



import sqlite3
from PIL import Image
from io import BytesIO

#
#
# def readSqliteTable():
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
#             img_data = row[1]
#             image = Image.open(BytesIO(img_data))
#             radius = row[2]
#             nPins = row[3]
#
#             # Create an instance of StringImageCircle with the values from the database
#             string_circle = StringImageCircle(image, radius, nPins)
#
#             # Do something with the StringImageCircle instance here
#             # For example:
#             string_circle.img.show()
#             print(f"radius: {string_circle.radius}, nPins: {string_circle.nPins}")
#             print("\n")
#
#         cursor.close()
#
#     except sqlite3.Error as error:
#         print("Failed to read data from sqlite table", error)
#     finally:
#         if sqliteConnection:
#             sqliteConnection.close()
#             print("The SQLite connection is closed")
#
#
#
#
#
#



class StringImageCircle:
    def __init__(self, img_path, radius, nPins):
        self.radius = radius
        self.nPins = nPins
        self.img, self.img_res = self.PrepareImage(img_path, radius)
        self.PinPos = self.PreparePins(radius, nPins)
        self.Lines = []

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
        return img, img_res

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
        return self.img_res


class StringImageSquare:
    def __init__(self, img_path, dimension, nPins, noise=5):
        self.dimension = dimension
        self.nPins = nPins
        self.noise = noise
        self.img, self.img_res = self.PrepareImage(img_path, dimension)
        self.PinPos = self.PreparePins(dimension)
        self.Lines = []

    def PrepareImage(self, img_path, dimension):
        im_t = Image.open(img_path).convert('L')
        w, h = im_t.size
        min_dim = min(h, w)
        top = int((h - min_dim) / 2)
        left = int((w - min_dim) / 2)
        im_croped = im_t.crop((left, top, left + min_dim, top + min_dim)).resize((dimension + 1, dimension + 1))
        img = np.asarray(im_croped).copy()

        img = 255 - img

        img_res = np.ones(img.shape) * 255
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
        print("getLineMask")
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
        print("FindBestNextPin")
        return bestPin, bestMean

    def SaveImage(self, image_matrix, file_path, description, color=(255, 0, 0), position=(10, 10)):
        imtemp = Image.fromarray(image_matrix).convert('RGB')
        drawer = ImageDraw.Draw(imtemp)
        font = ImageFont.truetype("font.ttf", 36)
        drawer.text(position, description, color, font=font)
        imtemp.save(file_path)
        print("SaveImage")

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
        print("Convert")
        return self.img_res




#Сюда подставляем данные
img_path = "112.png"
radius = 500
nPins = 400
nLines = 2000

# Usage



# def readSqliteTable():
#     conn = sqlite3.connect('stringart.db')
#     cursor = conn.cursor()
#
#     cursor.execute('SELECT image_data, nLines, nPins, radius FROM stringart')
#     row = cursor.fetchone()
#     img_data, nLines, nPins, radius = row
#     print(f"Виводить данние "
#           f"Количество линий: {nLines},"
#           f"Количество понов: {nPins},"
#           f"Радиус круга: {radius} ")
#
#
#
#     return img_data, nLines, nPins, radius
#
# img_data, nLines, nPins, radius = readSqliteTable()
#
# string_circle = StringImageCircle(img_data, radius, nPins)
# plt.imshow(string_circle.img_res, cmap='gray')
# plt.show()

if __name__ == '__main__':
    converter = StringImageCircle(img_path, radius, nPins)
    img_res = converter.Convert(max_lines=nLines)
    plt.imshow(img_res, cmap='gray')
    plt.show()


#
# import sqlite3
#
# # создание подключения к базе данных
# conn = sqlite3.connect('stringart.db')
#
# # создание объекта курсора
# cursor = conn.cursor()
#
# # выполнение запроса SQL
# cursor.execute("SELECT * FROM stringart")
#
# # извлечение результата запроса
# rows = cursor.fetchall()
# print(rows)
# # закрытие соединения с базой данных
# conn.close()