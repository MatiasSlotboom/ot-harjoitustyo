class Set:
    '''
    Represents a set of an exercise in a workout.

    Attributes:
        id: The ID of the set.
        exercise_id: The ID of the exercise associated with the set.
        set_number: The number of the set.
        repetitions: The number of repetitions for the set.
        weight: The weight used for the set.
    '''

    def __init__(
        self,
        exercise_id: int,
        set_number: int,
        repetitions: int,
        weight: float,
        set_id: int = None
    ):
        '''
        Initializes a Set object.
        Args:
            exercise_id: The ID of the exercise associated with the set.
            set_number: The number of the set.
            repetitions: The number of repetitions for the set.
            weight: The weight used for the set.
            set_id: An optional ID for the set (used when retrieving from the database).
        '''
        self.id = set_id
        self.exercise_id = exercise_id
        self.set_number = set_number
        self.repetitions = repetitions
        self.weight = weight
