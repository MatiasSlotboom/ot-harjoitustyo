import unittest

from build import build
from db.database_connection import get_database_connection
from repositories.exercise_repository import ExerciseRepository
from entities.exercise import Exercise


class TestExerciseRepository(unittest.TestCase):
    def setUp(self):
        build()
        self.exercise_repository = ExerciseRepository(get_database_connection())
        self.exercise_repository.delete_all()
        self.workout_id_1 = 101
        self.workout_id_2 = 102

        self.exercise_1 = Exercise(workout_id=self.workout_id_1, exercise_name="Push-ups", note="Standard")
        self.exercise_2 = Exercise(workout_id=self.workout_id_1, exercise_name="Squats", note="Bodyweight")
        self.exercise_3 = Exercise(workout_id=self.workout_id_2, exercise_name="Pull-ups", note="Assisted")

    def test_create_exercise(self):
        self.exercise_repository.create(self.exercise_1)

        found_exercises = self.exercise_repository.find_by_workout_id(self.workout_id_1)

        self.assertEqual(len(found_exercises), 1)
        found_excercise = found_exercises[0]
        self.assertIsNotNone(found_excercise.id)
        self.assertEqual(found_excercise.workout_id, self.exercise_1.workout_id)
        self.assertEqual(found_excercise.exercise_name, self.exercise_1.exercise_name)
        self.assertEqual(found_excercise.note, self.exercise_1.note)

    def test_find_by_workout_id_multiple_exercises(self):
        self.exercise_repository.create(self.exercise_1)
        self.exercise_repository.create(self.exercise_2)
        self.exercise_repository.create(self.exercise_3)

        found_exercises = self.exercise_repository.find_by_workout_id(self.workout_id_1)

        self.assertEqual(len(found_exercises), 2)
        found_names = {exercise.exercise_name for exercise in found_exercises}
        self.assertIn(self.exercise_1.exercise_name, found_names)
        self.assertIn(self.exercise_2.exercise_name, found_names)

        for exercise in found_exercises:
            self.assertEqual(exercise.workout_id, self.workout_id_1)

    def test_find_by_workout_id_no_exercises(self):
        found_exercises = self.exercise_repository.find_by_workout_id(999)
        self.assertEqual(len(found_exercises), 0)
        self.assertEqual(found_exercises, [])

    def test_find_by_id_exists(self):
        self.exercise_repository.create(self.exercise_1)
        
        all_for_workout = self.exercise_repository.find_by_workout_id(self.workout_id_1)
        created_id = all_for_workout[0].id 

        found_exercise = self.exercise_repository.find_by_id(created_id)

        self.assertIsNotNone(found_exercise)
        self.assertEqual(found_exercise.id, created_id)
        self.assertEqual(found_exercise.workout_id, self.exercise_1.workout_id)
        self.assertEqual(found_exercise.exercise_name, self.exercise_1.exercise_name)
        self.assertEqual(found_exercise.note, self.exercise_1.note)

    def test_find_by_id_not_exists(self):
        found_exercise = self.exercise_repository.find_by_id(999)
        self.assertIsNone(found_exercise)

    def test_update_exercise(self):
        self.exercise_repository.create(self.exercise_1)
        created_exercise = self.exercise_repository.find_by_workout_id(self.workout_id_1)[0]
        
        created_exercise.exercise_name = "Diamond Push-ups"
        created_exercise.note = "Close grip"

        updated_exercise_returned = self.exercise_repository.update(created_exercise)

        self.assertEqual(updated_exercise_returned.exercise_name, "Diamond Push-ups")
        self.assertEqual(updated_exercise_returned.note, "Close grip")

        fetched_after_update = self.exercise_repository.find_by_id(created_exercise.id)
        self.assertIsNotNone(fetched_after_update)
        self.assertEqual(fetched_after_update.exercise_name, "Diamond Push-ups")
        self.assertEqual(fetched_after_update.note, "Close grip")
        self.assertEqual(fetched_after_update.workout_id, self.workout_id_1)

    def test_update_exercise_no_id_raises_error(self):
        exercise_no_id = Exercise(workout_id=self.workout_id_1, exercise_name="Test", note="Note")
        
        self.assertIsNone(exercise_no_id.id) 
        
        with self.assertRaises(ValueError) as cm:
            self.exercise_repository.update(exercise_no_id)
        
        self.assertEqual(str(cm.exception), "Exercise must have an ID to be updated")

    def test_delete_exercise(self):
        self.exercise_repository.create(self.exercise_1)
        self.exercise_repository.create(self.exercise_2)

        exercises_before_delete = self.exercise_repository.find_by_workout_id(self.workout_id_1)
        id_to_delete = None
        for ex in exercises_before_delete:
            if ex.exercise_name == self.exercise_1.exercise_name:
                id_to_delete = ex.id
                break
        
        self.assertIsNotNone(id_to_delete, "Failed to find exercise to delete in setup")

        self.exercise_repository.delete(id_to_delete)

        found_exercise = self.exercise_repository.find_by_id(id_to_delete)
        self.assertIsNone(found_exercise)

        remaining_exercises = self.exercise_repository.find_by_workout_id(self.workout_id_1)
        self.assertEqual(len(remaining_exercises), 1)
        self.assertEqual(remaining_exercises[0].exercise_name, self.exercise_2.exercise_name)

    def test_delete_nonexistent_exercise(self):
        try:
            self.exercise_repository.delete(999)
        except Exception as e:
            self.fail(f"Deleting non-existent exercise raised an exception: {e}")

    def test_delete_all(self):
        self.exercise_repository.create(self.exercise_1)
        self.exercise_repository.create(self.exercise_2)
        self.exercise_repository.create(self.exercise_3)

        self.assertGreater(len(self.exercise_repository.find_by_workout_id(self.workout_id_1)), 0)
        self.assertGreater(len(self.exercise_repository.find_by_workout_id(self.workout_id_2)), 0)

        self.exercise_repository.delete_all()

        found_exercises_1 = self.exercise_repository.find_by_workout_id(self.workout_id_1)
        found_exercises_2 = self.exercise_repository.find_by_workout_id(self.workout_id_2)

        self.assertEqual(len(found_exercises_1), 0)
        self.assertEqual(len(found_exercises_2), 0)