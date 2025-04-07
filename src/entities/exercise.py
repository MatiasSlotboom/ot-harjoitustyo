class Exercise:
    def __init__(self, workout_id: int, exercise_name: str, note: str = None, id: int = None):
        self.id = id
        self.workout_id = workout_id
        self.exercise_name = exercise_name
        self.note = note
