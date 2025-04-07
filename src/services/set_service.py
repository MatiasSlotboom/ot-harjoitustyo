from repositories.set_repository import set_repository as default_set_repository
from entities.set import Set


class SetService:
    def __init__(self, set_repository=default_set_repository):
        self._set_repository = set_repository

    def add_set(self, exercise_id: int, set_number: int, repetitions: int, weight: float):
        set_instance = Set(exercise_id=exercise_id, set_number=set_number,
                           repetitions=repetitions, weight=weight)
        return self._set_repository.create(set_instance)

    def get_sets_for_exercise(self, exercise_id: int):
        return self._set_repository.find_by_exercise_id(exercise_id)

    def get_set_by_id(self, set_id: int):
        return self._set_repository.find_by_id(set_id)

    def update_set(self, set_id: int, new_set_number: int, new_repetitions: int, new_weight: float):
        set_instance = self._set_repository.find_by_id(set_id)
        if not set_instance:
            return None
        set_instance.set_number = new_set_number
        set_instance.repetitions = new_repetitions
        set_instance.weight = new_weight
        return self._set_repository.update(set_instance)

    def delete_set(self, set_id: int):
        self._set_repository.delete(set_id)


set_service = SetService()
