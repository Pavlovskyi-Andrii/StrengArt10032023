import sqlite3
from PIL import Image
from io import BytesIO

def readSqliteTable():
    try:
        sqliteConnection = sqlite3.connect('stringart.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from stringart"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print("Id: ", row[0])
            s1 = row[0]
            print("image_data: ", row[1])
            s2 = row[1]
            image = Image.open(BytesIO(s2))
            image.show()
            print(f"this image {image}")
            print("radius: ", row[2])
            s3 = row[2]
            print("nPins: ", row[3])
            s4 = row[3]
            print("nLines: ", row[4])
            s5 = row[4]
            print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")




# import sqlite3
#
# from PIL import Image
# from io import BytesIO
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
#             s1=row[0]
#             return s1
#
#             print("image_data: ", row[1])
#             s2=row[1]
#             return s2
#             image = Image.open(BytesIO(s2))
#             image.show()
#             return s2
#             print(f"this image {image})
#
#             print("radius: ", row[2])
#             s3 = row[2]
#             return s3
#
#             print("nPins: ", row[3])
#             s4 = row[3]
#             return s4
#
#             print("nLines: ", row[4])
#             s5 = row[4]
#             return s5
#
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
# # example_id = records.row[0]
# # print(example_id)
#
#
# readSqliteTable()