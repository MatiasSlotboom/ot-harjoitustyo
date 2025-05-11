from repositories.set_repository import set_repository as default_set_repository
from entities.set import Set


class SetService:
    def __init__(self, set_repository=default_set_repository):
        '''
        Initializes the SetService with a repository for set management.
        Args:
            set_repository: An instance of a set repository.
        '''
        self._set_repository = set_repository

    def add_set(self, exercise_id: int, set_number: int, repetitions: int, weight: float):
        '''
        Adds a new set to an exercise.
        Args:
            exercise_id: The ID of the exercise to add the set to.
            set_number: The number of the set.
            repetitions: The number of repetitions for the set.
            weight: The weight used for the set.
        Returns:
            The created Set object.
        '''
        set_instance = Set(exercise_id=exercise_id, set_number=set_number,
                           repetitions=repetitions, weight=weight)
        return self._set_repository.create(set_instance)

    def get_sets_for_exercise(self, exercise_id: int):
        '''
        Retrieves all sets associated with a specific exercise ID.
        Args:
            exercise_id: The ID of the exercise to find sets for.
        Returns:
            A list of Set objects associated with the exercise ID.
        '''
        return self._set_repository.find_by_exercise_id(exercise_id)

    def get_set_by_id(self, set_id: int):
        '''
        Retrieves a set by its ID.
        Args:
            set_id: The ID of the set to retrieve.
        Returns:
            A Set object with the specified ID.
        '''
        return self._set_repository.find_by_id(set_id)

    def update_set(self, set_id: int, new_set_number: int, new_repetitions: int, new_weight: float):
        '''
        Updates an existing set with a new set number, repetitions, and weight.
        Args:
            set_id: The ID of the set to update.
            new_set_number: The new set number.
            new_repetitions: The new number of repetitions.
            new_weight: The new weight for the set.
        Returns:
            The updated Set object.
        '''
        set_instance = self._set_repository.find_by_id(set_id)
        if not set_instance:
            return None
        set_instance.set_number = new_set_number
        set_instance.repetitions = new_repetitions
        set_instance.weight = new_weight
        return self._set_repository.update(set_instance)

    def delete_set(self, set_id: int):
        '''
        Deletes a set from the database by its ID.
        Args:
            set_id: The ID of the set to delete.
        '''
        self._set_repository.delete(set_id)


set_service = SetService()
