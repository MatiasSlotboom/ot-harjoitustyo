class Set:
    def __init__(self, exercise_id: int, set_number: int, repetitions: int, weight: float, id: int = None):
        self.id = id
        self.exercise_id = exercise_id
        self.set_number = set_number
        self.repetitions = repetitions
        self.weight = weight