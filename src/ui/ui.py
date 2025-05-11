from tkinter import Tk
from ui.workout_list_view import WorkoutListView
from ui.workout_view import WorkoutView


class UI:
    '''
    A class representing the main user interface of the workout tracking application.
    This class manages the different views of the application, including the workout list
    and workout details views.
    '''
    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):    
        '''
        Starts the UI by displaying the workout list view.
        '''
        self._show_workout_list_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()
        self._current_view = None

    def _show_workout_list_view(self):
        self._hide_current_view()
        self._current_view = WorkoutListView(
            self._root,
            self._show_workout_view_for_add,
            self._show_workout_view_for_edit
        )
        self._current_view.pack()

    def _show_workout_view_for_add(self):
        self._hide_current_view()

        self._current_view = WorkoutView(
            self._root,
            self._show_workout_list_view,
            None
        )
        self._current_view.pack()

    def _show_workout_view_for_edit(self, workout_id):
        self._hide_current_view()

        self._current_view = WorkoutView(
            self._root,
            self._show_workout_list_view,
            workout_id
        )
        self._current_view.pack()
