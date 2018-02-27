import tkinter as tk
from .dialog_window import DialogWindow


class SimpleDialog(DialogWindow):

    def __init__(self, app, mode):
        self.app = app
        super().__init__(app)
        text_label = {
            "win": app.language["win"],
            "lose": app.language["lose"],
            "restart": app.language["restart"],
            "quit": app.language["quit"],
            "info": app.language["info"]
            }
        yes_command = self.app.exit if mode == "quit" else self.app.restart
        no_command = self.app.exit if (mode == "win" or mode == "lose") else self.resume
        self.protocol("WM_DELETE_WINDOW", no_command)
        self.message = tk.Label(self.content, text=text_label[mode], padx=10, pady=10)
        self.message.grid(row=0, column=0, columnspan=2)
        if mode == "info":
            self.ok_button = tk.Button(self.content, command=self.resume, text=app.language["ok"], padx=10)
            self.ok_button.grid(row=1, column=0, columnspan=2)
            self.ok_button.focus_force()
            self.ok_button.bind("<Return>", self.resume)
        else:
            self.yes_button = tk.Button(self.content, command=yes_command, text=app.language["yes"], padx=10)
            self.yes_button.grid(row=1, column=0)
            self.yes_button.bind("<Return>", yes_command)
            self.no_button = tk.Button(self.content, command=no_command, text=app.language["no"], padx=10)
            self.no_button.grid(row=1, column=1)
            self.no_button.bind("<Return>", no_command)
            if mode == "win" or mode == "lose":
                self.yes_button.focus_force()
            else:
                self.no_button.focus_force()
            self.bind("<Right>", self.no_button_focus)
            self.bind("<Left>", self.yes_button_focus)

    def no_button_focus(self, event=None):
        self.no_button.focus_set()

    def yes_button_focus(self, event=None):
        self.yes_button.focus_set()
