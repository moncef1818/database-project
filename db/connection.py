import psycopg2

DATABASE = 'postgres'
USER = 'postgres'
PASSWORD = 'moncefmoussa'
HOST = 'localhost'
PORT = '5433'

def get_connection():

    connection = psycopg2.connect(
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )

    return connection

def close_connection(connection):
    if connection:
        connection.close()

def get_cursor(connection):
    if connection:
        return connection.cursor()
    return None

def main():
    conn = get_connection()
    cursor = get_cursor(conn)
    if(cursor is not None):
        print("Connection and cursor established.")
        cursor.execute("SELECT * from student;")
        data = cursor.fetchall()
        for d in data:
            print(d)
    close_connection(conn)
    print("Connection closed.")

if __name__ == "__main__":
    main()
