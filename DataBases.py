import sqlite3
from sqlite3 import Error
# from db import *


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Запрос выполенен успешно")
    except Error as e:
        print(f'Ошибка: {e}')


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f'Ошибка: {e}')


read_query = "SELECT word FROM main"
connection = create_connection("words.sqlite")

