import tkinter as tk


class DialogWindow(tk.Toplevel):

    def __init__(self, app):
        self.field = app.field
        super().__init__()
        self.withdraw()
        self.transient(app)
        self.resizable(0, 0)
        self.title(app.language["title"])
        self.content = tk.Frame(self, padx=10, pady=10)
        self.content.grid()

    # All the popup windows appears above main field.
    # By default the center of the dialog window
    # aligns with the center of the game field,
    # but if the dialog won't fit the screen it is shifted.
    def position(self):
        self.update_idletasks()
        field_x = self.field.winfo_rootx()
        field_y = self.field.winfo_rooty()
        field_width = self.field.winfo_width()
        field_height = self.field.winfo_height()
        dialog_width = self.winfo_reqwidth()
        dialog_height = self.winfo_reqheight()
        dialog_x = int(field_x + field_width / 2 - dialog_width / 2)
        dialog_y = int(field_y + field_height / 2 - dialog_height / 2)
        if dialog_x < 0:
            dialog_x = 0
        elif dialog_x > (self.winfo_screenwidth() - dialog_width):
            dialog_x = self.winfo_screenwidth() - dialog_width
        self.geometry("{}x{}+{}+{}".format(dialog_width, dialog_height,
                                           dialog_x, dialog_y))
        self.deiconify()
        self.grab_set()
        self.wait_window(self)

    def resume(self, event=None):
        self.destroy()
