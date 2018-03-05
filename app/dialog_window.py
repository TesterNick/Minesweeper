import tkinter as tk


class DialogWindow(tk.Toplevel):

    def __init__(self, app):
        self.field = app.field
        self.pause_the_game()
        super().__init__()
        self.resizable(0, 0)
        self.title(app.language["title"])
        self.bind("<FocusOut>", self.require_attention)
        self.content = tk.Frame(self, padx=10, pady=10)
        self.content.grid()

    def pause_the_game(self):
        for name in self.field.cells:
            cell = self.field.cells[name]
            cell.deactivate()

    def resume(self, event=None):
        self.destroy()
        for name in self.field.cells:
            cell = self.field.cells[name]
            cell.activate()

    def require_attention(self, event=None):
        self.bell()
        self.lift()
        self.focus_force()
