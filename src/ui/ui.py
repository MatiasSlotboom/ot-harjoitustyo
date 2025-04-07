from tkinter import Tk
from ui.workout_list_view import WorkoutListView
from ui.workout_view import WorkoutView


class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
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
