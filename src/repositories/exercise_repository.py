from db.database_connection import get_database_connection
from entities.exercise import Exercise


def get_exercise_by_row(row):
    if row:
        return Exercise(id=row["id"], workout_id=row["workout_id"], exercise_name=row["exercise_name"], note=row["note"])
    else:
        return None


class ExerciseRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, exercise):
        cursor = self._connection.cursor()
        cursor.execute(
            "insert into exercises (workout_id, exercise_name, note) values (?, ?, ?)",
            (exercise.workout_id, exercise.exercise_name, exercise.note)
        )
        self._connection.commit()
        return exercise

    def find_by_workout_id(self, workout_id):
        cursor = self._connection.cursor()
        cursor.execute(
            "select id, workout_id, exercise_name, note from exercises where workout_id = ?",
            (workout_id,)
        )
        rows = cursor.fetchall()
        return list(map(get_exercise_by_row, rows))

    def find_by_id(self, exercise_id):
        cursor = self._connection.cursor()
        cursor.execute(
             "select id, workout_id, exercise_name, note from exercises where id = ?",
             (exercise_id,)
        )
        row = cursor.fetchone()
        return get_exercise_by_row(row)

    def update(self, exercise):
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
        cursor = self._connection.cursor()
        cursor.execute("delete from exercises where id = ?", (exercise_id,))
        self._connection.commit()

    def delete_all(self):
        cursor = self._connection.cursor()
        cursor.execute("delete from exercises")
        self._connection.commit()


exercise_repository = ExerciseRepository(get_database_connection())