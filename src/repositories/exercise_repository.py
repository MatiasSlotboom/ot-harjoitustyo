from db.database_connection import get_database_connection
from entities.exercise import Exercise


def get_exercise_by_row(row):
    '''
    Converts a database row into a Set object.
    Args:
        row: A row from the database containing exercise data.
    Returns:
        A Exercise object with the data from the row.
    '''
    if row:
        return Exercise(
            excercise_id=row["id"],
            workout_id=row["workout_id"],
            exercise_name=row["exercise_name"],
            note=row["note"]
        )
    return None


class ExerciseRepository:
    '''Repository class for managing Exercise entities in the database.'''

    def __init__(self, connection):
        '''
        Initializes the repository with a database connection.
        Args:
            connection: A database connection object.
        '''
        self._connection = connection

    def create(self, exercise):
        '''
        Inserts a new Exercise into the database.
        Args:
            exercise: An Exercise object to be inserted.
        Returns:
            The inserted Exercise object with its ID populated.
        '''
        cursor = self._connection.cursor()
        cursor.execute(
            "insert into exercises (workout_id, exercise_name, note) values (?, ?, ?) returning id",
            (exercise.workout_id, exercise.exercise_name, exercise.note)
        )

        exercise.id = cursor.fetchone()[0]
        self._connection.commit()
        return exercise

    def find_by_workout_id(self, workout_id):
        '''
        Retrieves all Exercises associated with a specific workout ID.
        Args:
            workout_id: The ID of the workout to find exercises for.
        Returns:
            A list of Exercise objects associated with the workout ID.
        '''
        cursor = self._connection.cursor()
        cursor.execute(
            "select id, workout_id, exercise_name, note from exercises where workout_id = ?",
            (workout_id,)
        )
        rows = cursor.fetchall()
        return list(map(get_exercise_by_row, rows))

    def find_by_id(self, exercise_id):
        '''
        Retrieves an Exercise by its ID.
        Args:
            exercise_id: The ID of the exercise to retrieve.
        '''
        cursor = self._connection.cursor()
        cursor.execute(
            "select id, workout_id, exercise_name, note from exercises where id = ?",
            (exercise_id,)
        )
        row = cursor.fetchone()
        return get_exercise_by_row(row)

    def update(self, exercise):
        '''
        Updates an existing Exercise in the database.
        Args:
            exercise: An Exercise object with updated values.
        Returns:
            The updated Exercise object.
        '''
        if exercise.id is None:
            raise ValueError("Exercise must have an ID to be updated")
        cursor = self._connection.cursor()
        cursor.execute(
            "update exercises set exercise_name = ?, note = ? where id = ?",
            (exercise.exercise_name, exercise.note, exercise.id)
        )
        self._connection.commit()
        return exercise

    def delete(self, exercise_id):
        '''
        Deletes an Exercise from the database by its ID.
        Args:
            exercise_id: The ID of the exercise to delete.
        '''
        cursor = self._connection.cursor()
        cursor.execute("delete from exercises where id = ?", (exercise_id,))
        self._connection.commit()

    def delete_all(self):
        '''
        Deletes all Exercises from the database.
        '''
        cursor = self._connection.cursor()
        cursor.execute("delete from exercises")
        self._connection.commit()


exercise_repository = ExerciseRepository(get_database_connection())
