from repositories.workout_repository import workout_repository as default_workout_repository
from repositories.exercise_repository import exercise_repository as default_exercise_repository
from repositories.set_repository import set_repository as default_set_repository
from entities.workout import Workout


class WorkoutService:
    def __init__(
        self,
        workout_repository=default_workout_repository,
        exercise_repository=default_exercise_repository,
        set_repository=default_set_repository
    ):
        self._workout_repository = workout_repository
        self._exercise_repository = exercise_repository
        self._set_repository = set_repository

    def create_workout(self, workout_date: str):
        workout = Workout(workout_date=workout_date)
        return self._workout_repository.create(workout)

    def get_all_workouts(self):
        return self._workout_repository.find_all()

    def get_workout_by_id(self, workout_id: int):
        return self._workout_repository.find_by_id(workout_id)

    def update_workout_date(self, workout_id: int, new_date: str):
        workout = self._workout_repository.find_by_id(workout_id)
        if not workout:
            return None
        workout.workout_date = new_date
        return self._workout_repository.update(workout)

    def delete_workout(self, workout_id: int):
        self._workout_repository.delete(workout_id)

    def get_full_workout_details(self, workout_id: int):
        workout = self._workout_repository.find_by_id(workout_id)
        if not workout:
            return None
        exercises = self._exercise_repository.find_by_workout_id(workout_id)
        full_exercises_details = []
        for exercise in exercises:
            sets = self._set_repository.find_by_exercise_id(exercise.id)
            full_exercises_details.append({'exercise': exercise, 'sets': sets})
        return {'workout': workout, 'exercises': full_exercises_details}

workout_service = WorkoutService()