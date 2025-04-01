from tkinter import Toplevel, Label, Entry, Button, Frame, StringVar


class EntryDialog(Toplevel):
    def __init__(self, parent, title, fields):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)
        self.parent = parent
        self.result = None
        self.fields = fields
        self.entries = {}

        body = Frame(self)
        self.initial_focus = self._body(body)
        body.pack(padx=5, pady=5)

        self._buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self._cancel)
        self.geometry(f"+{parent.winfo_rootx()+50}+{parent.winfo_rooty()+50}")
        self.initial_focus.focus_set()
        self.wait_window(self)

    def _body(self, master):
        row_num = 0
        for label_text, initial_value in self.fields.items():
            lbl = Label(master, text=f"{label_text}:")
            lbl.grid(row=row_num, column=0, sticky='w', padx=5, pady=2)
            entry_var = StringVar(master, value=initial_value)
            entry = Entry(master, textvariable=entry_var, width=30)
            entry.grid(row=row_num, column=1, padx=5, pady=2)
            self.entries[label_text] = entry_var
            row_num += 1
        return self.entries.get(list(self.fields.keys())[0])

    def _buttonbox(self):
        box = Frame(self)
        ok_button = Button(box, text="OK", width=10, command=self._ok, default='active')
        ok_button.pack(side='left', padx=5, pady=5)
        cancel_button = Button(box, text="Cancel", width=10, command=self._cancel)
        cancel_button.pack(side='left', padx=5, pady=5)
        self.bind("<Return>", self._ok)
        self.bind("<Escape>", self._cancel)
        box.pack()

    def _ok(self, event=None):
        self.result = {label: var.get() for label, var in self.entries.items()}
        self.withdraw()
        self.update_idletasks()
        self.parent.focus_set()
        self.destroy()

    def _cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()