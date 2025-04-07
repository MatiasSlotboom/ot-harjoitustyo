from tkinter import ttk, constants, Listbox, Scrollbar, messagebox
from services.workout_service import workout_service


class WorkoutListView:
    def __init__(self, root, handle_add_workout, handle_view_edit_workout):
        self._root = root
        self._handle_add_workout = handle_add_workout
        self._handle_view_edit_workout = handle_view_edit_workout
        self._frame = None
        self._listbox = None
        self._workout_map = {}

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        list_label = ttk.Label(master=self._frame, text="Saved Workouts:")
        list_label.pack(pady=5)

        list_frame = ttk.Frame(master=self._frame)
        list_frame.pack(fill=constants.BOTH, expand=True, padx=10, pady=5)

        scrollbar = Scrollbar(master=list_frame, orient=constants.VERTICAL)
        self._listbox = Listbox(
            master=list_frame, yscrollcommand=scrollbar.set, height=15)
        scrollbar.config(command=self._listbox.yview)
        scrollbar.pack(side=constants.RIGHT, fill=constants.Y)
        self._listbox.pack(side=constants.LEFT,
                           fill=constants.BOTH, expand=True)
        self._listbox.bind("<Double-Button-1>",
                           self._handle_view_edit_selected)

        button_frame = ttk.Frame(master=self._frame)
        button_frame.pack(fill=constants.X, padx=10, pady=10)

        add_button = ttk.Button(
            master=button_frame,
            text="Add New Workout",
            command=self._handle_add_workout
        )
        view_edit_button = ttk.Button(
            master=button_frame,
            text="View/Edit Selected",
            command=self._handle_view_edit_selected
        )
        delete_button = ttk.Button(
            master=button_frame,
            text="Delete Selected",
            command=self._handle_delete_selected
        )

        add_button.pack(side=constants.LEFT, padx=5)
        view_edit_button.pack(side=constants.LEFT, padx=5)
        delete_button.pack(side=constants.LEFT, padx=5)

        self._load_workouts()

    def _load_workouts(self):
        self._listbox.delete(0, constants.END)
        self._workout_map.clear()
        workouts = workout_service.get_all_workouts()
        if workouts:
            for index, workout in enumerate(workouts):
                display_text = f"{workout.workout_date} (ID: {workout.id})"
                self._listbox.insert(index, display_text)
                self._workout_map[index] = workout.id

    def _handle_view_edit_selected(self, event=None):
        selected_indices = self._listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Required",
                                   "Please select a workout from the list.")
            return
        selected_index = selected_indices[0]
        if selected_index in self._workout_map:
            workout_id = self._workout_map[selected_index]
            self._handle_view_edit_workout(workout_id)

    def _handle_delete_selected(self):
        selected_indices = self._listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Required",
                                   "Please select a workout to delete.")
            return

        selected_index = selected_indices[0]
        if selected_index in self._workout_map:
            workout_id = self._workout_map[selected_index]
            workout = workout_service.get_workout_by_id(workout_id)
            if not workout:
                messagebox.showerror(
                    "Error", f"Workout with ID {workout_id} not found.")
                self._load_workouts()
                return

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete the workout from {workout.workout_date} (ID: {workout_id})?\nThis will also delete all its exercises and sets."
            )
            if confirm:
                try:
                    workout_service.delete_workout(workout_id)
                    messagebox.showinfo(
                        "Success", "Workout deleted successfully.")
                    self._load_workouts()
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"Failed to delete workout: {e}")
