class Exercise:
    '''
    Represents an exercise in a workout.

    Attributes:
        id: The ID of the exercise.
        workout_id: The ID of the workout associated with the exercise.
        exercise_name: The name of the exercise.
        note: An optional note for the exercise.
    '''

    def __init__(self, workout_id: int, exercise_name: str, note: str = None, excercise_id: int = None):
        '''
        Initializes an Exercise object.
        Args:
            workout_id: The ID of the workout associated with the exercise.
            exercise_name: The name of the exercise.
            note: An optional note for the exercise.
            excercise_id: An optional ID for the exercise (used when retrieving from the database).
        '''
        self.id = excercise_id
        self.workout_id = workout_id
        self.exercise_name = exercise_name
        self.note = note
