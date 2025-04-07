from db.database_connection import get_database_connection


def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("drop table if exists sets;")
    cursor.execute("drop table if exists exercises;")
    cursor.execute("drop table if exists workouts;")

    connection.commit()


def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_date TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER NOT NULL,
            exercise_name TEXT NOT NULL,
            note TEXT,
            FOREIGN KEY (workout_id) REFERENCES workouts (id) ON DELETE CASCADE
        );
    """)

    cursor.execute("""
        CREATE TABLE sets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_id INTEGER NOT NULL,
            set_number INTEGER NOT NULL,
            repetitions INTEGER NOT NULL,
            weight REAL NOT NULL,
            FOREIGN KEY (exercise_id) REFERENCES exercises (id) ON DELETE CASCADE
        );
    """)

    connection.commit()


def initialise_database():
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)
    if connection:
        connection.close()


if __name__ == "__main__":
    initialise_database()
