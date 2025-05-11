from db.database_connection import get_database_connection
from entities.workout import Workout


def get_workout_by_row(row):
    '''
    Converts a database row into a Workout object.
    Args:
        row: A row from the database containing workout data.
    Returns:
        A Workout object with the data from the row.
    '''
    if row:
        return Workout(workout_id=row["id"], workout_date=row["workout_date"])
    return None


class WorkoutRepository:
    '''Repository class for managing Workout entities in the database.'''

    def __init__(self, connection):
        self._connection = connection

    def create(self, workout):
        '''
        Inserts a new Workout into the database.
        Args:
            workout: A Workout object to be inserted.
        Returns:
            The inserted Workout object with its ID populated.
        '''
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO workouts (workout_date) VALUES (?)",
            (workout.workout_date,)
        )
        self._connection.commit()
        workout.id = cursor.lastrowid
        return workout

    def find_all(self):
        '''
        Retrieves all Workouts from the database.
        Returns:
            A list of Workout objects.
        '''
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, workout_date FROM workouts ORDER BY workout_date DESC")
        rows = cursor.fetchall()
        return [get_workout_by_row(row) for row in rows]

    def find_by_id(self, workout_id):
        '''
        Retrieves a Workout by its ID.
        Args:
            workout_id: The ID of the workout to find.
        Returns:
            A Workout object with the specified ID.
        '''
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, workout_date FROM workouts WHERE id = ?",
            (workout_id,)
        )
        row = cursor.fetchone()
        return get_workout_by_row(row)

    def update(self, workout):
        '''
        Updates an existing Workout in the database.
        Args:
            workout: A Workout object with updated data.
        Returns:
            The updated Workout object.
        '''
        if workout.id is None:
            raise ValueError("Workout must have an ID to be updated")
        cursor = self._connection.cursor()
        cursor.execute(
            "UPDATE workouts SET workout_date = ? WHERE id = ?",
            (workout.workout_date, workout.id)
        )
        self._connection.commit()
        return workout

    def delete(self, workout_id):
        '''
        Deletes a Workout from the database by its ID.
        Args:
            workout_id: The ID of the workout to delete.
        '''
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
        self._connection.commit()

    def delete_all(self):
        '''
        Deletes all Workouts from the database.
        '''
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM workouts")
        self._connection.commit()


workout_repository = WorkoutRepository(get_database_connection())
