from tkinter import ttk, constants, StringVar, messagebox
from ui.dialog import EntryDialog
from services.workout_service import workout_service
from services.exercise_service import exercise_service
from services.set_service import set_service
import datetime


class WorkoutView:
    def __init__(self, root, handle_back, workout_id=None):
        self._root = root
        self._handle_back = handle_back
        self._workout_id = workout_id
        self._workout_date_var = StringVar()
        self._exercises_tree = None
        self._frame = None
        self._exercise_map = {}
        self._set_map = {}

        self._initialize()
        self._load_workout_data()

    def pack(self):
        self._frame.pack(fill=constants.BOTH, expand=True)

    def destroy(self):
        self._frame.destroy()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        top_frame = ttk.Frame(master=self._frame)
        top_frame.pack(fill=constants.X, padx=10, pady=5)

        back_button = ttk.Button(
            master=top_frame, text="< Back to List", command=self._handle_back)
        back_button.pack(side=constants.LEFT)

        date_label = ttk.Label(
            master=top_frame, text="Workout Date (YYYY-MM-DD HH:MM:SS):")
        date_label.pack(side=constants.LEFT, padx=(20, 5))
        date_entry = ttk.Entry(
            master=top_frame, textvariable=self._workout_date_var, width=25)
        date_entry.pack(side=constants.LEFT)

        save_workout_button = ttk.Button(
            master=top_frame, text="Save Workout", command=self._handle_save_workout)
        save_workout_button.pack(side=constants.RIGHT, padx=10)

        tree_frame = ttk.Frame(master=self._frame)
        tree_frame.pack(fill=constants.BOTH, expand=True, padx=10, pady=5)

        self._exercises_tree = ttk.Treeview(
            master=tree_frame,
            columns=("type", "name_note", "set_num",
                     "reps", "weight", "weightlb"),
            show="tree headings"
        )

        vsb = ttk.Scrollbar(master=tree_frame, orient="vertical",
                            command=self._exercises_tree.yview)
        hsb = ttk.Scrollbar(master=tree_frame, orient="horizontal",
                            command=self._exercises_tree.xview)
        self._exercises_tree.configure(
            yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self._exercises_tree.heading("#0", text="Item")
        self._exercises_tree.heading("type", text="Type")
        self._exercises_tree.heading("name_note", text="Name / Note")
        self._exercises_tree.heading("set_num", text="Set #")
        self._exercises_tree.heading("reps", text="Reps")
        self._exercises_tree.heading("weight", text="Weight (kg)")
        self._exercises_tree.heading("weightlb", text="Weight (lb)")

        self._exercises_tree.column("#0", width=50, stretch=False)
        self._exercises_tree.column("type", width=80, anchor='center')
        self._exercises_tree.column("name_note", width=200)
        self._exercises_tree.column("set_num", width=60, anchor='center')
        self._exercises_tree.column("reps", width=60, anchor='center')
        self._exercises_tree.column("weight", width=80, anchor='center')
        self._exercises_tree.column("weightlb", width=80, anchor='center')

        vsb.pack(side=constants.RIGHT, fill=constants.Y)
        hsb.pack(side=constants.BOTTOM, fill=constants.X)
        self._exercises_tree.pack(fill=constants.BOTH, expand=True)
        self._exercises_tree.bind("<Double-Button-1>",
                                  self._handle_edit_selected)

        action_frame = ttk.Frame(master=self._frame)
        action_frame.pack(fill=constants.X, padx=10, pady=10)

        add_exercise_button = ttk.Button(
            master=action_frame, text="Add Exercise", command=self._handle_add_exercise)
        edit_button = ttk.Button(
            master=action_frame, text="Edit Selected", command=self._handle_edit_selected)
        delete_button = ttk.Button(
            master=action_frame, text="Delete Selected", command=self._handle_delete_selected)
        add_set_button = ttk.Button(
            master=action_frame, text="Add Set to Selected Exercise", command=self._handle_add_set)

        add_exercise_button.pack(side=constants.LEFT, padx=5)
        add_set_button.pack(side=constants.LEFT, padx=5)
        edit_button.pack(side=constants.LEFT, padx=5)
        delete_button.pack(side=constants.LEFT, padx=5)

    def _load_workout_data(self):
        for item in self._exercises_tree.get_children():
            self._exercises_tree.delete(item)
        self._exercise_map.clear()
        self._set_map.clear()

        if self._workout_id:
            details = workout_service.get_full_workout_details(
                self._workout_id)
            if details and details['workout']:
                workout = details['workout']
                self._workout_date_var.set(workout.workout_date)

                if details['exercises']:
                    for ex_detail in details['exercises']:
                        exercise = ex_detail['exercise']
                        sets = ex_detail['sets']

                        ex_item_id = self._exercises_tree.insert(
                            "",
                            constants.END,
                            text=f"E{exercise.id}",
                            values=("Exercise", exercise.exercise_name,
                                    "", "", "", ""),
                            open=True
                        )
                        self._exercise_map[ex_item_id] = exercise.id

                        if exercise.note:
                            self._exercises_tree.insert(ex_item_id, constants.END, text="Note", values=(
                                "Note", exercise.note, "", "", ""))

                        if sets:
                            for set_instance in sets:
                                set_item_id = self._exercises_tree.insert(
                                    ex_item_id,
                                    constants.END,
                                    text=f"S{set_instance.id}",
                                    values=("Set", "", set_instance.set_number,
                                            set_instance.repetitions, set_instance.weight, round(set_instance.weight*2.20462262, 2))
                                )
                                self._set_map[set_item_id] = set_instance.id
            else:
                messagebox.showerror(
                    "Error", f"Could not load details for workout ID {self._workout_id}.")
                self._handle_back()
        else:
            now = datetime.datetime.now()
            default_date = now.strftime('%Y-%m-%d %H:%M:%S')
            self._workout_date_var.set(default_date)

    def _handle_save_workout(self):
        date_str = self._workout_date_var.get()
        try:
            parsed_date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            formatted_date_str = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            messagebox.showerror(
                "Invalid Date", "enter the date in YYYY-MM-DD HH:MM:SS format.")
            return

        try:
            if self._workout_id:
                workout_service.update_workout_date(self._workout_id, formatted_date_str)
                messagebox.showinfo(
                    "Saved", "Workout date updated. Exercises/Sets are saved via their respective Add/Edit actions.")
            else:
                new_workout = workout_service.create_workout(formatted_date_str)
                self._workout_id = new_workout.id
                messagebox.showinfo(
                    "Created", f"New workout created with ID: {self._workout_id}. You can now add exercises and sets.")
            self._workout_date_var.set(formatted_date_str)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save workout: {e}")

    def _handle_add_exercise(self):
        if not self._workout_id:
            self._handle_save_workout()

        dialog = EntryDialog(self._frame, "Add Exercise", {
                             "Name": "", "Note (optional)": ""})
        if dialog.result:
            name = dialog.result.get("Name")
            note = dialog.result.get("Note (optional)")
            if name:
                try:
                    exercise_service.add_exercise(
                        self._workout_id, name, note if note else None)
                    self._load_workout_data()
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"Failed to add exercise: {e}")
            else:
                messagebox.showwarning(
                    "Input Required", "Exercise name cannot be empty.")

    def _handle_add_set(self):
        selected_item = self._exercises_tree.focus()
        if not selected_item:
            messagebox.showwarning(
                "Selection Required", "select an Exercise item in the tree to add a set to.")
            return

        if selected_item in self._exercise_map:
            exercise_id = self._exercise_map[selected_item]

            sets = set_service.get_sets_for_exercise(exercise_id)
            next_set_num = len(sets) + 1

            dialog = EntryDialog(self._frame, f"Add Set {next_set_num}", {
                                 "Reps": "", "Weight (kg)": ""})
            if dialog.result:
                try:
                    reps = int(dialog.result.get("Reps", 0))
                    weight = float(dialog.result.get("Weight (kg)", 0.0))
                    if reps < 0 or weight < 0:
                        raise ValueError("Values must be non-negative")

                    set_service.add_set(
                        exercise_id, next_set_num, reps, weight)
                    self._load_workout_data()
                except ValueError:
                    messagebox.showerror(
                        "Invalid Input", "enter valid numbers (integer for Reps, number for Weight).")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add set: {e}")
        else:
            messagebox.showwarning(
                "Select Exercise", "select an Exercise item (not a Set or Note) to add a set to.")

    def _handle_edit_selected(self, event=None):
        selected_item = self._exercises_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Required",
                                   "select an Exercise or Set to edit.")
            return

        if selected_item in self._exercise_map:
            exercise_id = self._exercise_map[selected_item]
            exercise = exercise_service.get_exercise_by_id(exercise_id)
            if not exercise:
                messagebox.showerror(
                    "Error", "Could not find selected exercise.")
                self._load_workout_data()
                return

            dialog = EntryDialog(self._frame, "Edit Exercise", {
                                 "Name": exercise.exercise_name, "Note": exercise.note if exercise.note else ""})
            if dialog.result:
                name = dialog.result.get("Name")
                note = dialog.result.get("Note")
                if name:
                    try:
                        exercise_service.update_exercise(
                            exercise_id, name, note if note else None)
                        self._load_workout_data()
                    except Exception as e:
                        messagebox.showerror(
                            "Error", f"Failed to update exercise: {e}")
                else:
                    messagebox.showwarning(
                        "Input Required", "Exercise name cannot be empty.")

        elif selected_item in self._set_map:
            set_id = self._set_map[selected_item]
            set_instance = set_service.get_set_by_id(set_id)
            if not set_instance:
                messagebox.showerror("Error", "Could not find selected set.")
                self._load_workout_data()
                return

            dialog = EntryDialog(self._frame, f"Edit Set {set_instance.set_number}", {
                                 "Reps": str(set_instance.repetitions), "Weight (kg)": str(set_instance.weight)})
            if dialog.result:
                try:
                    reps = int(dialog.result.get("Reps", 0))
                    weight = float(dialog.result.get("Weight (kg)", 0.0))
                    if reps < 0 or weight < 0:
                        raise ValueError("Values must be non-negative")

                    set_service.update_set(
                        set_id, set_instance.set_number, reps, weight)
                    self._load_workout_data()
                except ValueError:
                    messagebox.showerror(
                        "Invalid Input", "enter valid numbers (integer for Reps, number for Weight).")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update set: {e}")
        else:
            pass

    def _handle_delete_selected(self):
        selected_item = self._exercises_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Required",
                                   "select an Exercise or Set to delete.")
            return

        if selected_item in self._exercise_map:
            exercise_id = self._exercise_map[selected_item]
            exercise = exercise_service.get_exercise_by_id(exercise_id)
            name = exercise.exercise_name if exercise else f"ID {exercise_id}"
            confirm = messagebox.askyesno(
                "Confirm Delete", f"Delete Exercise '{name}' and ALL its sets?")
            if confirm:
                try:
                    exercise_service.delete_exercise(exercise_id)
                    self._load_workout_data()
                except Exception as e:
                    messagebox.showerror(
                        "Error", f"Failed to delete exercise: {e}")

        elif selected_item in self._set_map:
            set_id = self._set_map[selected_item]
            set_instance = set_service.get_set_by_id(set_id)
            confirm_msg = f"Delete Set #{set_instance.set_number} ({set_instance.repetitions} reps @ {set_instance.weight}kg)?" if set_instance else f"Delete Set ID {set_id}?"
            confirm = messagebox.askyesno("Confirm Delete", confirm_msg)
            if confirm:
                try:
                    set_service.delete_set(set_id)
                    self._load_workout_data()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete set: {e}")
        else:
            messagebox.showwarning(
                "Invalid Selection", "Cannot delete this item type (e.g., Note). Select an Exercise or Set.")
