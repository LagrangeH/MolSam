import sqlite3
from sqlite3 import Error
from db import *


# Todo: create class DataBase
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Успешное подключение к базе данных")
    except Error as e:
        print(f'Ошибка: {e}')

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Запрос выполенен успешно")
    except Error as e:
        print(f'Ошибка: {e}')


connection = create_connection("words.sqlite")
# execute_query(connection, dat)
