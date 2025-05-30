class Workout:
    '''
    Represents a workout session.
    Attributes:
        id: The ID of the workout.
        workout_date: The date of the workout.
    '''

    def __init__(self, workout_date: str, workout_id: int = None):
        '''
        Initializes a Workout object.
        Args:
            workout_date: The date of the workout.
            workout_id: An optional ID for the workout (used when retrieving from the database).
        '''
        self.id = workout_id
        self.workout_date = workout_date
