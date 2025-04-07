from repositories.exercise_repository import exercise_repository as default_exercise_repository
from entities.exercise import Exercise


class ExerciseService:
    def __init__(self, exercise_repository=default_exercise_repository):
        self._exercise_repository = exercise_repository

    def add_exercise(self, workout_id: int, exercise_name: str, note: str = None):
        exercise = Exercise(workout_id=workout_id,
                            exercise_name=exercise_name, note=note)
        return self._exercise_repository.create(exercise)

    def get_exercises_for_workout(self, workout_id: int):
        return self._exercise_repository.find_by_workout_id(workout_id)

    def get_exercise_by_id(self, exercise_id: int):
        return self._exercise_repository.find_by_id(exercise_id)

    def update_exercise(self, exercise_id: int, new_name: str, new_note: str = None):
        exercise = self._exercise_repository.find_by_id(exercise_id)
        if not exercise:
            return None
        exercise.exercise_name = new_name
        exercise.note = new_note
        return self._exercise_repository.update(exercise)

    def delete_exercise(self, exercise_id: int):
        self._exercise_repository.delete(exercise_id)


exercise_service = ExerciseService()
