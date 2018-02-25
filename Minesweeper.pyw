#!/usr/bin/env python3
"""
This is my version of popular game Minesweeper. It has GUI and requires Tcl/Tk installed on your system
as well as tkinter module in your Python library (included by default in standard package for Windows).

It is the second version of the program because it has GUI while the first one was completely textual.

Now you can play the game on your job even if sysadmins deleted
all the games before you got your computer :)

If you find some typos or bugs please don't hesitate to report them.
"""
import locale
import math
import random
import sys
import tkinter as tk


class Application(tk.Frame):

    def __init__(self, settings=None):
        self.root = tk.Tk()
        super().__init__()
        if settings is None:
            self.settings = Settings()
        self.language = self.settings.language
        self.root.resizable(0, 0)
        self.root.config(menu=self.create_menu(self.root))
        self.root.title(self.language["title"])
        self.root.protocol("WM_DELETE_WINDOW", self.ensure_exit)
        self.grid()
        self.field = Field(self.root, self.settings.get_field_settings())

    # Main menu
    def create_menu(self, root):
        m = tk.Menu(root)
        game = tk.Menu(m, tearoff=0)
        m.add_cascade(label=self.language["game"], menu=game)
        game.add_command(label=self.language["new"], command=self.ensure_restart)
        game.add_command(label=self.language["settings"], command=self.settings.change_settings_dialog)
        game.add_command(label=self.language["exit"], command=self.ensure_exit)
        about = tk.Menu(m, tearoff=0)
        m.add_cascade(label=self.language["about"], menu=about)
        about.add_command(label=self.language["version"], command=self.show_info)
        return m

    @staticmethod
    def ensure_restart():
        SimpleDialog("restart")

    @staticmethod
    def ensure_exit():
        SimpleDialog("quit")

    @staticmethod
    def lose():
        SimpleDialog("lose")

    @staticmethod
    def win():
        SimpleDialog("win")

    @staticmethod
    def show_info():
        SimpleDialog("info")


class Cell:

    def __init__(self, row, column, value):
        self.row = str(row)
        self.column = str(column)
        self.value = str(value)

    def automated_opening(self, event=None):
        neighbours = app.field.get_neighbours(self.column + self.row)
        # button_text = app.field.buttons[self.column + self.row].cget("text")
        if self.is_closed() and not self.is_bomb():
            amount_of_opened_nearby_bombs = 0
            for n in neighbours:
                if app.field.cells[n].is_marked():
                    amount_of_opened_nearby_bombs += 1
            if str(amount_of_opened_nearby_bombs) == self.value:
                for n in neighbours:
                    if app.field.buttons[n].cget("state") != "disabled":
                        app.field.cells[n].open_cell()
        for n in neighbours:
            cell = app.field.cells[n]
            if not cell.is_closed() or cell.is_marked():
                app.field.buttons[n].configure(relief="raised")

    def is_bomb(self):
        return self.value == "!"

    def is_closed(self):
        return app.field.buttons[self.column + self.row].cget("text") != ""

    def is_marked(self):
        return app.field.buttons[self.column + self.row].cget("text") == "X"

    def open_cell(self):
        button = app.field.buttons[self.column + self.row]
        if not self.is_marked():
            if self.is_bomb():
                button.configure(bg="red")
                app.lose()
            button.configure(text=self.value, state="disabled", relief="sunken")
            if self.value == " ":
                self.open_zeros()

    # Function recursively checks if the cell has no bombs around and opens them
    def open_zeros(self):
        neighbours = app.field.get_neighbours(self.column + self.row)
        for n in neighbours:
            cell = app.field.cells[n]
            if not cell.is_closed():
                cell.open_cell()
                if cell.value == " ":
                    cell.open_zeros()

    def mark_cell(self, event=None):
        if app.field.buttons[self.column + self.row].cget("state") != "disabled":
            if app.field.buttons[self.column + self.row].cget("text") == "":
                app.field.buttons[self.column + self.row].configure(text="X", disabledforeground="black")
                app.field.number_of_bombs -= 1
            else:
                color = app.field.color_chooser(self.column + self.row)
                app.field.buttons[self.column + self.row].configure(text="", disabledforeground=color)
                app.field.number_of_bombs += 1
            app.field.bomb_counter.configure(text=app.field.number_of_bombs)
            if app.field.number_of_bombs == 0:
                app.field.check()

    def two_buttons(self, event=None):
        if not self.is_marked():
            neighbours = app.field.get_neighbours(self.column + self.row)
            for n in neighbours:
                button = app.field.buttons[n]
                if not (button.cget("text") == "X" or button.cget("state") == "disabled"):
                    button.configure(relief="sunken")

    def mouse_leave(self, event=None):
        neighbours = app.field.get_neighbours(self.column + self.row)
        for n in neighbours:
            if app.field.buttons[n].cget("text") == "":
                app.field.buttons[n].configure(relief="raised")


class DialogWindow(tk.Toplevel):

    def __init__(self):
        for name in app.field.buttons:
            app.field.buttons[name].configure(state="disabled")
        super().__init__()
        self.resizable(0, 0)
        self.title(app.language["title"])
        self.content = tk.Frame(self, padx=10, pady=10)
        self.content.grid()


class SimpleDialog(DialogWindow):

    def __init__(self, mode):
        super().__init__()
        text_label = {
            "win": app.language["win"],
            "lose": app.language["lose"],
            "restart": app.language["restart"],
            "quit": app.language["quit"],
            "info": app.language["info"]
            }
        yes_command = self.exit if mode == "quit" else self.restart
        no_command = self.exit if (mode == "win" or mode == "lose") else self.resume
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
            self.no_button = tk.Button(self.content, command=no_command, text=app.language["no"], padx=8)
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

    def resume(self, event=None):
        self.withdraw()
        for name in app.field.buttons:
            if app.field.buttons[name].cget("text") == "X" or app.field.buttons[name].cget("text") == "":
                color = app.field.color_chooser(name)
                app.field.buttons[name].configure(state="normal", disabledforeground=color)

    def restart(self, event=None):
        self.withdraw()
        app.field = Field(app.root, app.settings.get_field_settings())

    def exit(self, event=None):
        self.withdraw()
        app.root.destroy()
        sys.exit()


class SettingsDialog(DialogWindow):

    def __init__(self):
        super().__init__()
        settings = app.settings
        self.protocol("WM_DELETE_WINDOW", self.discard_settings)
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
                                               command=self.discard_settings, width=10)
        self.content.cancel_button.grid(row=4, column=1)
        self.content.ok_button = tk.Button(self.content, text=settings.language["ok"],
                                           command=self.apply_settings_and_close, width=10)
        self.content.ok_button.grid(row=4, column=4)

    def apply_settings_and_close(self):
        listbox_value = self.content.lang_listbox.curselection()
        app.settings.apply_temp_settings(listbox_value)
        app.root.withdraw()
        app.__init__(app.settings)
        self.withdraw()

    def discard_settings(self):
        self.withdraw()
        for name in app.field.buttons:
            if app.field.buttons[name].cget("text") == "X" or app.field.buttons[name].cget("text") == "":
                color = app.field.color_chooser(name)
                app.field.buttons[name].configure(state="normal", disabledforeground=color)

    def update_no_of_bombs_widget(self, number=None):
        settings = app.settings
        new_maximum = math.floor(settings.temp_rows.get() * settings.temp_columns.get() * 0.8)
        settings.max_no_of_bombs.set(new_maximum)
        self.content.bombs_scale.configure(to=new_maximum)


class Field(tk.Frame):

    def __init__(self, master, settings):
        super().__init__()
        self.master = master
        self.cells = {}
        self.buttons = {}
        self.columns, self.rows, self.number_of_bombs = settings
        self.bomb_counter = tk.Label(master, text=self.number_of_bombs, font="courier 15 bold", fg="red")
        self.bomb_counter.grid(column=0, columnspan=len(self.columns), row=0)
        self.create_field(master)

    # Field creation and configuration
    def create_field(self, root):
        for i in range(self.rows):
            for j in self.columns:
                self.cells[j+str(i)] = Cell(i, j, " ")
        counter = 0
        # Placing bombs
        while counter < self.number_of_bombs:
            i = int(math.floor(random.random() * self.rows))
            j = self.columns[int(math.floor(random.random() * len(self.columns)))]
            if not self.cells[j+str(i)].is_bomb():
                self.cells[j+str(i)].value = "!"
                counter += 1
        # Filling non-bomb cells with numbers of nearby bombs
        for i in range(self.rows):
            for j in self.columns:
                cell = self.cells[j+str(i)]
                if not cell.is_bomb():
                    counter = 0
                    neighbours = self.get_neighbours(j+str(i))
                    for n in neighbours:
                        if self.cells[n].is_bomb():
                            counter += 1
                    if counter == 0:
                        cell.value = " "
                    else:
                        cell.value = str(counter)
        # Creating buttons for cells
        for i in range(self.rows):
            for j in self.columns:
                name = j+str(i)
                color = self.color_chooser(name)
                self.buttons[name] = tk.Button(root, command=self.cells[name].open_cell, disabledforeground=color,
                                               width=1, height=1, font="arial 12 bold", takefocus=0)
                self.buttons[name].bind("<ButtonRelease-3>", self.cells[name].mark_cell)
                self.buttons[name].bind("<Button-2>", self.cells[name].two_buttons)
                self.buttons[name].bind("<ButtonRelease-2>", self.cells[name].automated_opening)
                self.buttons[name].bind("<Leave>", self.cells[name].mouse_leave)
                self.buttons[name].bind("<B2-Motion>", self.cells[name].two_buttons)
        for cell in self.buttons:
            self.buttons[cell].grid(column=self.columns.index(cell[0]), row=(int(cell[1:]) + 1), ipadx=6)

    # Function return list of cell's names that are neighbours of the current cell
    def get_neighbours(self, coordinates):
        neighbours = []
        column = self.columns.index(coordinates[0])
        row = int(coordinates[1:])
        for i in range(row-1, row+2):
            for j in range(column-1, column+2):
                if (0 <= i < self.rows) and (0 <= j < len(self.columns)):
                    if not (i == row and j == column):
                        j = self.columns[j]
                        neighbours.append(j+str(i))
        return neighbours

    # Checking if all the bombs marked correctly
    def check(self):
        for name in self.buttons:
            if self.cells[name].is_bomb() and self.buttons[name].cget("text") == "":
                self.cells[name].open_cell()
                return
        app.win()

    # Choosing color of the digits
    def color_chooser(self, name):
        color = {
            " ": "grey",
            "1": "blue",
            "2": "green",
            "3": "red",
            "4": "dark blue",
            "5": "dark red",
            "6": "cyan",
            "7": "DarkMagenta",
            "8": "magenta",
            "!": "black"
            }[str(self.cells[name].value)]
        return color


class Settings(object):

    def __init__(self):
        self.version = "2.0.0b"
        self.rows = 10
        self.temp_rows = tk.IntVar()
        self.temp_rows.set(self.rows)
        self.columns = 10
        self.temp_columns = tk.IntVar()
        self.temp_columns.set(self.columns)
        self.number_of_bombs = 20
        self.temp_no_of_bombs = tk.IntVar()
        self.available_columns = "abcdefghijklmnopqrstuvwxyz"
        self.russian = {
            "about": "О программе",
            "bombs": "Количество бомб",
            "cancel": "Отмена",
            "exit": "Выход",
            "game": "Игра",
            "height": "Высота",
            "info": "Текущая версия программы\n{}".format(self.version),
            "language": "Язык",
            "lose": "К сожалению, вы проиграли. Хотите попробовать еще раз?",
            "new": "Новая",
            "no": "Нет",
            "ok": "ОК",
            "quit": "Вы уверены, что хотите выйти из игры?",
            "restart": "Вы уверены, что хотите начать новую игру?",
            "settings": "Настройки",
            "title": "Сапер от Ника",
            "version": "Версия",
            "width": "Ширина",
            "win": "Поздравляем! Вы выиграли! Сыграем еще раз?",
            "yes": "Да"
        }

        self.english = {
            "about": "About",
            "bombs": "Number of bombs",
            "cancel": "Cancel",
            "exit": "Exit",
            "game": "Game",
            "height": "Height",
            "info": "Current version is\n{}".format(self.version),
            "language": "Language",
            "lose": "Sorry, you've lost. Do you want to play again?",
            "new": "New",
            "no": "No",
            "ok": "OK",
            "quit": "Are you sure you want to exit?",
            "restart": "Are you sure you want to start new game?",
            "settings": "Settings",
            "title": "Nick's minesweeper",
            "version": "Version",
            "width": "Width",
            "win": "Congratulations! You've won! Do you want to play again?",
            "yes": "Yes"
        }
        self.langs = {
            "English": self.english,
            "Русский": self.russian
        }
        self.lang_list = [x for x in self.langs]
        self.temp_lang = tk.StringVar(value=self.lang_list)
        self.language = self.default_language()
        self.min_height = 5
        self.max_height = 20
        self.min_width = 5
        self.max_width = 30
        self.min_no_of_bombs = 3
        self.max_no_of_bombs = tk.IntVar()
        self.max_no_of_bombs.set(math.floor(self.temp_rows.get() * self.temp_columns.get() * 0.8))

    def apply_temp_settings(self, listbox_value):
        self.rows = self.temp_rows.get()
        self.columns = self.temp_columns.get()
        self.number_of_bombs = self.temp_no_of_bombs.get()
        try:
            self.language = self.langs[self.lang_list[listbox_value[0]]]
        except IndexError:
            pass

    @staticmethod
    def change_settings_dialog():
        SettingsDialog()

    def default_language(self):
        if locale.getdefaultlocale()[0].lower() == "ru_ru":
            return self.russian
        else:
            return self.english

    def get_field_settings(self):
        return self.available_columns[:self.columns], self.rows, self.number_of_bombs


app = Application()
app.mainloop()
