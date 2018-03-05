import math
import tkinter as tk
from .dialog_window import DialogWindow


class SettingsDialog(DialogWindow):

    def __init__(self, app):
        super().__init__(app)
        self.app = app
        settings = self.app.settings
        self.protocol("WM_DELETE_WINDOW", self.resume)
        # Width control
        self.content.width_label = tk.Label(self.content, padx=10, pady=10, text=settings.language["width"])
        self.content.width_label.grid(row=0, column=0)
        self.content.width_scale = tk.Scale(self.content, orient="horizontal", variable=settings.temp_columns,
                                            showvalue=False, from_=settings.min_width, to=settings.max_width,
                                            command=self.update_no_of_bombs_widget)
        self.content.width_scale.grid(row=0, column=1, columnspan=2)
        self.content.width_value = tk.Label(self.content, padx=10, pady=10, textvariable=settings.temp_columns)
        self.content.width_value.grid(row=0, column=4)

        # Height control
        self.content.height_label = tk.Label(self.content, padx=10, pady=10, text=settings.language["height"])
        self.content.height_label.grid(row=1, column=0)
        self.content.height_scale = tk.Scale(self.content, orient="horizontal", variable=settings.temp_rows,
                                             showvalue=False, from_=settings.min_height, to=settings.max_height,
                                             command=self.update_no_of_bombs_widget)
        self.content.height_scale.grid(row=1, column=1, columnspan=2)
        self.content.height_value = tk.Label(self.content, padx=10, pady=10, textvariable=settings.temp_rows)
        self.content.height_value.grid(row=1, column=4)

        # Bombs control
        self.content.bombs_label = tk.Label(self.content, padx=10, pady=10, text=settings.language["bombs"])
        self.content.bombs_label.grid(row=2, column=0)
        settings.temp_no_of_bombs.set(settings.number_of_bombs)
        self.content.bombs_scale = tk.Scale(self.content, orient="horizontal", showvalue=False,
                                            variable=settings.temp_no_of_bombs,
                                            from_=settings.min_no_of_bombs,
                                            to=settings.max_no_of_bombs.get())
        self.content.bombs_scale.grid(row=2, column=1, columnspan=2)
        self.content.bombs_value = tk.Label(self.content, padx=10, pady=10, textvariable=settings.temp_no_of_bombs)
        self.content.bombs_value.grid(row=2, column=4)

        # Language control
        self.content.lang_label = tk.Label(self.content, padx=10, pady=10, text=settings.language["language"])
        self.content.lang_label.grid(row=3, column=0)
        self.content.lang_listbox = tk.Listbox(self.content, listvariable=settings.temp_lang,
                                               selectmode="single", height=0)
        self.content.lang_listbox.grid(row=3, column=1)

        # Main buttons
        self.content.cancel_button = tk.Button(self.content, text=settings.language["cancel"],
                                               command=self.resume, width=10)
        self.content.cancel_button.grid(row=4, column=1)
        self.content.ok_button = tk.Button(self.content, text=settings.language["ok"],
                                           command=self.apply_settings_and_close, width=10)
        self.content.ok_button.grid(row=4, column=4)

    def apply_settings_and_close(self):
        listbox_value = self.content.lang_listbox.curselection()
        self.app.settings.apply_temp_settings(listbox_value)
        self.app.restart()

    def update_no_of_bombs_widget(self, number=None):
        settings = self.app.settings
        new_maximum = math.floor(settings.temp_rows.get() * settings.temp_columns.get() * 0.75)
        settings.max_no_of_bombs.set(new_maximum)
        self.content.bombs_scale.configure(to=new_maximum)
