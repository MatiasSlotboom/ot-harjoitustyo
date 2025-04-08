import unittest

from build import build
from db.database_connection import get_database_connection
from repositories.workout_repository import WorkoutRepository
from repositories.exercise_repository import ExerciseRepository
from repositories.set_repository import SetRepository
from entities.workout import Workout
from entities.exercise import Exercise
from entities.set import Set
from services.workout_service import WorkoutService


class TestWorkoutService(unittest.TestCase):
    def setUp(self):
        build()
        self.connection = get_database_connection()
        self.workout_repository = WorkoutRepository(self.connection)
        self.exercise_repository = ExerciseRepository(self.connection)
        self.set_repository = SetRepository(self.connection)

        self.set_repository.delete_all()
        self.exercise_repository.delete_all()
        self.workout_repository.delete_all()

        self.workout_service = WorkoutService(
            workout_repository=self.workout_repository,
            exercise_repository=self.exercise_repository,
            set_repository=self.set_repository
        )

        self.sample_date_1 = "2024-03-10"
        self.sample_date_2 = "2024-03-11"

    def tearDown(self):
        if self.connection:
            self.connection.close()

    def test_create_workout(self):
        created_workout = self.workout_service.create_workout(
            workout_date=self.sample_date_1)

        self.assertIsNotNone(created_workout)
        self.assertIsNotNone(created_workout.id)
        self.assertEqual(created_workout.workout_date, self.sample_date_1)

        fetched_workout = self.workout_repository.find_by_id(
            created_workout.id)
        self.assertIsNotNone(fetched_workout)
        self.assertEqual(fetched_workout.id, created_workout.id)
        self.assertEqual(fetched_workout.workout_date, self.sample_date_1)

    def test_get_all_workouts(self):
        workout1 = self.workout_repository.create(
            Workout(workout_date=self.sample_date_1))
        workout2 = self.workout_repository.create(
            Workout(workout_date=self.sample_date_2))

        all_workouts = self.workout_service.get_all_workouts()

        self.assertEqual(len(all_workouts), 2)
        found_ids = {w.id for w in all_workouts}
        self.assertIn(workout1.id, found_ids)
        self.assertIn(workout2.id, found_ids)
        found_dates = {w.workout_date for w in all_workouts}
        self.assertIn(self.sample_date_1, found_dates)
        self.assertIn(self.sample_date_2, found_dates)

    def test_get_workout_by_id_exists(self):
        created_workout = self.workout_service.create_workout(
            workout_date=self.sample_date_1)
        workout_id = created_workout.id

        found_workout = self.workout_service.get_workout_by_id(workout_id)

        self.assertIsNotNone(found_workout)
        self.assertEqual(found_workout.id, workout_id)
        self.assertEqual(found_workout.workout_date, self.sample_date_1)

    def test_get_workout_by_id_not_exists(self):
        non_existent_id = 99999
        found_workout = self.workout_service.get_workout_by_id(non_existent_id)
        self.assertIsNone(found_workout)

    def test_update_workout_date_exists(self):
        created_workout = self.workout_service.create_workout(
            workout_date=self.sample_date_1)
        workout_id = created_workout.id
        new_date = "2025-01-01"

        updated_workout = self.workout_service.update_workout_date(
            workout_id, new_date)

        self.assertIsNotNone(updated_workout)
        self.assertEqual(updated_workout.id, workout_id)
        self.assertEqual(updated_workout.workout_date, new_date)

        fetched_workout = self.workout_repository.find_by_id(workout_id)
        self.assertIsNotNone(fetched_workout)
        self.assertEqual(fetched_workout.workout_date, new_date)

    def test_update_workout_date_not_exists(self):
        non_existent_id = 99999
        new_date = "2025-01-01"

        updated_workout = self.workout_service.update_workout_date(
            non_existent_id, new_date)

        self.assertIsNone(updated_workout)

    def test_delete_workout(self):
        workout_to_delete = self.workout_service.create_workout(
            workout_date=self.sample_date_1)
        workout_id_to_delete = workout_to_delete.id

        exercise = self.exercise_repository.create(Exercise(
            workout_id=workout_id_to_delete, exercise_name="Test Ex", note="Note"))

        self.set_repository.create(Set(
            exercise_id=exercise.id, set_number=1, repetitions=10, weight=50.0))
        self.workout_service.delete_workout(workout_id_to_delete)

        deleted_workout_check = self.workout_repository.find_by_id(
            workout_id_to_delete)
        self.assertIsNone(deleted_workout_check)

    def test_get_full_workout_details_exists(self):
        workout = self.workout_service.create_workout(
            workout_date=self.sample_date_1)
        workout_id = workout.id

        exercise1 = self.exercise_repository.create(Exercise(
            workout_id=workout_id, exercise_name="Push-ups", note="Standard"))
        exercise2 = self.exercise_repository.create(Exercise(
            workout_id=workout_id, exercise_name="Squats", note="Bodyweight"))

        set1_ex1 = self.set_repository.create(
            Set(exercise_id=exercise1.id, set_number=1, repetitions=15, weight=0.0))
        set2_ex1 = self.set_repository.create(
            Set(exercise_id=exercise1.id, set_number=2, repetitions=12, weight=0.0))
        set1_ex2 = self.set_repository.create(
            Set(exercise_id=exercise2.id, set_number=1, repetitions=20, weight=0.0))

        full_details = self.workout_service.get_full_workout_details(
            workout_id)

        self.assertIsNotNone(full_details)
        self.assertEqual(full_details['workout'].id, workout_id)
        self.assertEqual(
            full_details['workout'].workout_date, self.sample_date_1)

        self.assertEqual(len(full_details['exercises']), 2)

        ex1_details = next(
            (ex for ex in full_details['exercises'] if ex['exercise'].id == exercise1.id), None)
        self.assertIsNotNone(ex1_details)
        self.assertEqual(ex1_details['exercise'].exercise_name, "Push-ups")
        self.assertEqual(len(ex1_details['sets']), 2)
        set_ids_ex1 = {s.id for s in ex1_details['sets']}
        self.assertIn(set1_ex1.id, set_ids_ex1)
        self.assertIn(set2_ex1.id, set_ids_ex1)

        ex2_details = next(
            (ex for ex in full_details['exercises'] if ex['exercise'].id == exercise2.id), None)
        self.assertIsNotNone(ex2_details)
        self.assertEqual(ex2_details['exercise'].exercise_name, "Squats")
        self.assertEqual(len(ex2_details['sets']), 1)
        self.assertEqual(ex2_details['sets'][0].id, set1_ex2.id)

    def test_get_full_workout_details_workout_not_found(self):
        non_existent_id = 99999
        full_details = self.workout_service.get_full_workout_details(
            non_existent_id)
        self.assertIsNone(full_details)

    def test_get_full_workout_details_no_exercises(self):
        workout = self.workout_service.create_workout(
            workout_date=self.sample_date_1)
        workout_id = workout.id

        full_details = self.workout_service.get_full_workout_details(
            workout_id)

        self.assertIsNotNone(full_details)
        self.assertEqual(full_details['workout'].id, workout_id)
        self.assertEqual(len(full_details['exercises']), 0)
        self.assertEqual(full_details['exercises'], [])
