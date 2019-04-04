import math
import tkinter as tk
from .dialog_window import DialogWindow


class SettingsDialog(DialogWindow):

    def __init__(self, app):
        super().__init__(app)
        self.app = app
        settings = self.app.settings
        self.protocol("WM_DELETE_WINDOW", self.resume)
        c = self.content
        # Width control
        c.width_label = tk.Label(c, padx=10, pady=10,
                                 text=settings.language["width"])
        c.width_label.grid(row=0, column=0)
        c.width_scale = tk.Scale(c, orient="horizontal", showvalue=False,
                                 variable=settings.tmp_cols,
                                 from_=settings.min_width,
                                 to=settings.max_width,
                                 command=self.update_no_of_bombs_widget)
        c.width_scale.grid(row=0, column=1, columnspan=2)
        c.width_value = tk.Label(c, padx=10, pady=10,
                                 textvariable=settings.tmp_cols)
        c.width_value.grid(row=0, column=4)

        # Height control
        c.height_label = tk.Label(c, padx=10, pady=10,
                                  text=settings.language["height"])
        c.height_label.grid(row=1, column=0)
        c.height_scale = tk.Scale(c, orient="horizontal", showvalue=False,
                                  variable=settings.tmp_rows,
                                  from_=settings.min_height,
                                  to=settings.max_height,
                                  command=self.update_no_of_bombs_widget)
        c.height_scale.grid(row=1, column=1, columnspan=2)
        c.height_value = tk.Label(c, padx=10, pady=10,
                                  textvariable=settings.tmp_rows)
        c.height_value.grid(row=1, column=4)

        # Bombs control
        c.bombs_label = tk.Label(c, padx=10, pady=10,
                                 text=settings.language["bombs"])
        c.bombs_label.grid(row=2, column=0)
        settings.temp_no_of_bombs.set(settings.number_of_bombs)
        c.bombs_scale = tk.Scale(c, orient="horizontal", showvalue=False,
                                 variable=settings.temp_no_of_bombs,
                                 from_=settings.min_no_of_bombs,
                                 to=settings.max_no_of_bombs.get())
        c.bombs_scale.grid(row=2, column=1, columnspan=2)
        c.bombs_value = tk.Label(c, padx=10, pady=10,
                                 textvariable=settings.temp_no_of_bombs)
        c.bombs_value.grid(row=2, column=4)

        # Language control
        c.lang_label = tk.Label(c, padx=10, pady=10,
                                text=settings.language["language"])
        c.lang_label.grid(row=3, column=0)
        c.lang_listbox = tk.Listbox(c, listvariable=settings.temp_lang,
                                    selectmode="single", height=0)
        c.lang_listbox.grid(row=3, column=1)

        # Main buttons
        c.cancel_button = tk.Button(c, text=settings.language["cancel"],
                                    command=self.resume, width=10)
        c.cancel_button.grid(row=4, column=1)
        c.cancel_button.focus_force()
        c.ok_button = tk.Button(c, text=settings.language["ok"],
                                command=self.apply_settings_and_close, width=10)
        c.ok_button.grid(row=4, column=4)
        self.position()

    def apply_settings_and_close(self):
        listbox_value = self.content.lang_listbox.curselection()
        self.app.settings.apply_temp_settings(listbox_value)
        self.app.restart()

    def update_no_of_bombs_widget(self, number=None):
        settings = self.app.settings
        new_maximum = settings.get_temp_max_no_of_bombs()
        settings.max_no_of_bombs.set(new_maximum)
        self.content.bombs_scale.configure(to=new_maximum)
