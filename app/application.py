import gc
import tkinter as tk
from .simple_dialog import SimpleDialog
from .field import Field
from .settings import Settings


class Application(tk.Frame):

    def __init__(self, parent, settings=None):
        super().__init__()
        if settings is None:
            self.settings = Settings(self)
        else:
            self.settings = settings
        self.language = self.settings.language
        self.parent = parent
        self.parent.resizable(0, 0)
        self.parent.protocol("WM_DELETE_WINDOW", self.ensure_exit)
        self.parent.config(menu=self.create_menu(self))
        self.parent.title(self.language["title"])
        self.grid()
        self.field = Field(self, self.settings)

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

    def exit(self, event=None):
        self.parent.quit()

    def restart(self, event=None):
        for child in self.parent.winfo_children():
            child.destroy()
        self.__init__(self.parent, self.settings)
