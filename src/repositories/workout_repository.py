from db.database_connection import get_database_connection
from entities.workout import Workout


def get_workout_by_row(row):
    return Workout(id=row["id"], workout_date=row["workout_date"]) if row else None


class WorkoutRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, workout):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO workouts (workout_date) VALUES (?)",
            (workout.workout_date,)
        )
        self._connection.commit()
        workout.id = cursor.lastrowid
        return workout

    def find_all(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT id, workout_date FROM workouts ORDER BY workout_date DESC")
        rows = cursor.fetchall()
        return [get_workout_by_row(row) for row in rows]

    def find_by_id(self, workout_id):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, workout_date FROM workouts WHERE id = ?",
            (workout_id,)
        )
        row = cursor.fetchone()
        return get_workout_by_row(row)

    def update(self, workout):
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
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
        self._connection.commit()

    def delete_all(self):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM workouts")
        self._connection.commit()


workout_repository = WorkoutRepository(get_database_connection())