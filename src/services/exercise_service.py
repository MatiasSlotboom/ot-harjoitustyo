from repositories.exercise_repository import exercise_repository as default_exercise_repository
from entities.exercise import Exercise


class ExerciseService:
    def __init__(self, exercise_repository=default_exercise_repository):
        '''
        Initializes the ExerciseService with a repository for exercise management.
        Args:
            exercise_repository: An instance of an exercise repository.
        '''
        self._exercise_repository = exercise_repository

    def add_exercise(self, workout_id: int, exercise_name: str, note: str = None):
        '''
        Adds a new exercise to a workout.
        Args:
            workout_id: The ID of the workout to add the exercise to.
            exercise_name: The name of the exercise.
            note: An optional note for the exercise.
        Returns:
            The created Exercise object.
        '''
        exercise = Exercise(workout_id=workout_id,
                            exercise_name=exercise_name, note=note)
        return self._exercise_repository.create(exercise)

    def get_exercises_for_workout(self, workout_id: int):
        '''
        Retrieves all exercises associated with a specific workout ID.
        Args:
            workout_id: The ID of the workout to find exercises for.
        Returns:
            A list of Exercise objects associated with the workout ID.
        '''
        return self._exercise_repository.find_by_workout_id(workout_id)

    def get_exercise_by_id(self, exercise_id: int):
        '''
        Retrieves an exercise by its ID.
        Args:
            exercise_id: The ID of the exercise to retrieve.
        Returns:
            An Exercise object with the specified ID.
        '''
        return self._exercise_repository.find_by_id(exercise_id)

    def update_exercise(self, exercise_id: int, new_name: str, new_note: str = None):
        '''
        Updates an existing exercise with a new name and note.
        Args:
            exercise_id: The ID of the exercise to update.
            new_name: The new name for the exercise.
            new_note: An optional new note for the exercise.
        Returns:
            The updated Exercise object.
        '''
        exercise = self._exercise_repository.find_by_id(exercise_id)
        if not exercise:
            return None
        exercise.exercise_name = new_name
        exercise.note = new_note
        return self._exercise_repository.update(exercise)

    def delete_exercise(self, exercise_id: int):
        '''
        Deletes an exercise from the database by its ID.
        Args:
            exercise_id: The ID of the exercise to delete.
        '''
        self._exercise_repository.delete(exercise_id)


exercise_service = ExerciseService()
