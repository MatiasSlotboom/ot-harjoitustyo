from db.database_connection import get_database_connection
from entities.set import Set


def get_set_by_row(row):
    if row:
        return Set(id=row["id"], exercise_id=row["exercise_id"], set_number=row["set_number"], repetitions=row["repetitions"], weight=row["weight"])
    else:
        return None


class SetRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, set_obj):
        cursor = self._connection.cursor()
        cursor.execute(
            "insert into sets (exercise_id, set_number, repetitions, weight) values (?, ?, ?, ?)",
            (set_obj.exercise_id, set_obj.set_number,
             set_obj.repetitions, set_obj.weight)
        )
        self._connection.commit()
        return set_obj

    def find_by_exercise_id(self, exercise_id):
        cursor = self._connection.cursor()
        cursor.execute(
            "select id, exercise_id, set_number, repetitions, weight from sets where exercise_id = ? order by set_number asc",
            (exercise_id,)
        )
        rows = cursor.fetchall()
        return list(map(get_set_by_row, rows))

    def find_by_id(self, set_id):
        cursor = self._connection.cursor()
        cursor.execute(
            "select id, exercise_id, set_number, repetitions, weight from sets where id = ?",
            (set_id,)
        )
        row = cursor.fetchone()
        return get_set_by_row(row)

    def update(self, set_obj):
        if set_obj.id is None:
            raise ValueError("Set must have an ID to be updated")
        cursor = self._connection.cursor()
        cursor.execute(
            "update sets set set_number = ?, repetitions = ?, weight = ? where id = ?",
            (set_obj.set_number, set_obj.repetitions, set_obj.weight, set_obj.id)
        )
        self._connection.commit()
        return set_obj

    def delete(self, set_id):
        cursor = self._connection.cursor()
        cursor.execute("delete from sets where id = ?", (set_id,))
        self._connection.commit()

    def delete_all(self):
        cursor = self._connection.cursor()
        cursor.execute("delete from sets")
        self._connection.commit()


set_repository = SetRepository(get_database_connection())
