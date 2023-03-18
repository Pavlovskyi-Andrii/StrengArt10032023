import sqlite3
import time

# установление соединения с базой данных
conn = sqlite3.connect('stringart.db')
cursor = conn.cursor()

# добавление задержки
time.sleep(1)

# удаление таблицы
cursor.execute('DROP TABLE IF EXISTS stringart')

# сохранение изменений
conn.commit()

# закрытие соединения с базой данных
conn.close()