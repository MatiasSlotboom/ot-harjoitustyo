from db.database_connection import get_database_connection
from entities.set import Set


def get_set_by_row(row):
    '''
    Converts a database row into a Set object.
    Args:
        row: A row from the database containing set data.
    Returns:
        A Set object with the data from the row.
    '''
    if row:
        return Set(id=row["id"], exercise_id=row["exercise_id"],
                   set_number=row["set_number"], repetitions=row["repetitions"], weight=row["weight"])
    return None


class SetRepository:
    '''Repository class for managing Set entities in the database.'''

    def __init__(self, connection):
        '''
        Initializes the repository with a database connection.
        Args:
            connection: A database connection object.
        '''
        self._connection = connection

    def create(self, set_obj):
        '''
        Inserts a new Set into the database.
        Args:
            set_obj: A Set object to be inserted.
        Returns:
            The inserted Set object with its ID populated.
        '''
        cursor = self._connection.cursor()
        cursor.execute(
            "insert into sets (exercise_id, set_number, repetitions, weight) values (?, ?, ?, ?) returning id",
            (set_obj.exercise_id, set_obj.set_number,
             set_obj.repetitions, set_obj.weight)
        )
        set_obj.id = cursor.fetchone()[0]
        self._connection.commit()
        return set_obj

    def find_by_exercise_id(self, exercise_id):
        '''
        Retrieves all Sets associated with a specific exercise ID.
        Args:
            exercise_id: The ID of the exercise to find sets for.
        Returns:
            A list of Set objects associated with the exercise ID.
        '''
        cursor = self._connection.cursor()
        cursor.execute(
            "select id, exercise_id, set_number, repetitions, weight from sets where exercise_id = ? order by set_number asc",
            (exercise_id,)
        )
        rows = cursor.fetchall()
        return list(map(get_set_by_row, rows))

    def find_by_id(self, set_id):
        '''
        Retrieves a Set by its ID.
        Args:
            set_id: The ID of the set to retrieve.
        Returns:
            A Set object with the data from the row.
        '''
        cursor = self._connection.cursor()
        cursor.execute(
            "select id, exercise_id, set_number, repetitions, weight from sets where id = ?",
            (set_id,)
        )
        row = cursor.fetchone()
        return get_set_by_row(row)

    def update(self, set_obj):
        '''
        Updates an existing Set in the database.
        Args:
            set_obj: A Set object with updated values.
        Returns:
            The updated Set object.
        '''
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
        '''
        Deletes a Set from the database by its ID.
        Args:
            set_id: The ID of the set to delete.
        '''
        cursor = self._connection.cursor()
        cursor.execute("delete from sets where id = ?", (set_id,))
        self._connection.commit()

    def delete_all(self):
        '''
        Deletes all Sets from the database.
        '''
        cursor = self._connection.cursor()
        cursor.execute("delete from sets")
        self._connection.commit()


set_repository = SetRepository(get_database_connection())
