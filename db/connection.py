import psycopg2

DATABASE = "university"
USER = "postgres"
PASSWORD = "moncefmoussa"
HOST = "localhost"
PORT = "5433"


def get_connection():

    connection = psycopg2.connect(
        database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT
    )

    return connection


def close_connection(connection):
    if connection:
        connection.close()


def get_cursor(connection):
    if connection:
        return connection.cursor()
    return None


def close_cursor(cursor):
    if cursor:
        cursor.close()
