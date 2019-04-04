import tkinter as tk
from .field import Field
from .image_keeper import ImageKeeper
from .settings import Settings
from .simple_dialog import SimpleDialog


class Application(tk.Frame):

    def __init__(self, parent):
        super().__init__()
        self.settings = Settings(self)
        self.images = ImageKeeper()
        self.language = None
        self.parent = parent
        self.parent.resizable(0, 0)
        self.parent.protocol("WM_DELETE_WINDOW", self.ensure_exit)
        self.field = None
        self.create_window()

    def create_window(self):
        self.language = self.settings.language
        self.parent.config(menu=self.create_menu(self))
        self.parent.title(self.language["title"])
        self.field = Field(self, self.settings, self.images)

    # Main menu
    def create_menu(self, master):
        m = tk.Menu(master)
        game = tk.Menu(m, tearoff=0)
        m.add_cascade(label=self.language["game"], menu=game)
        game.add_command(label=self.language["new"], command=self.ensure_restart)
        game.add_command(label=self.language["settings"], command=self.settings.change_settings_dialog)
        game.add_command(label=self.language["exit"], command=self.ensure_exit)
        about = tk.Menu(m, tearoff=0)
        m.add_cascade(label=self.language["about"], menu=about)
        about.add_command(label=self.language["version"], command=self.show_info)
        return m

    def ensure_restart(self):
        SimpleDialog(self, "restart")

    def ensure_exit(self):
        SimpleDialog(self, "quit")

    def show_info(self):
        SimpleDialog(self, "info")

    def lose(self):
        self.field.show_the_bombs()
        SimpleDialog(self, "lose")

    def win(self):
        self.field.show_the_bombs()
        SimpleDialog(self, "win")

    def exit(self):
        for child in self.parent.winfo_children():
            child.destroy()
        self.parent.quit()

    def restart(self):
        for child in self.parent.winfo_children():
            if child != self:
                child.destroy()
        for cell in self.field.cells.keys():
            self.field.cells[cell] = None
        self.field = None
        self.create_window()
