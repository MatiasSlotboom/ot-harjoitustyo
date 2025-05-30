import sqlite3
from config import DATABASE_FILE_PATH

connection = sqlite3.connect(DATABASE_FILE_PATH)
connection.row_factory = sqlite3.Row


def get_database_connection():
    '''
    Establishes a connection to the database.
    Returns:
        connection: The database connection object.
    '''
    global connection
    try:
        connection.execute("SELECT 1;")
    except sqlite3.DatabaseError:
        connection = sqlite3.connect(DATABASE_FILE_PATH)
        connection.row_factory = sqlite3.Row

    return connection
