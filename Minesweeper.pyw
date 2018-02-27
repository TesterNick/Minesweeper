#!/usr/bin/env python3
"""
This is my version of popular game Minesweeper. It has GUI and requires Tcl/Tk installed on your system
as well as tkinter module in your Python library (included by default in standard package for Windows).

It is the second version of the program because it has GUI while the first one was completely textual.

Now you can play the game on your job even if sysadmins deleted
all the games before you got your computer :)

If you find some typos or bugs please don't hesitate to report them.
"""
import gc
import locale
import math
import os
import random
import tkinter as tk


class Application(tk.Frame):

    def __init__(self, parent, settings=None):
        super().__init__()
        if settings is None:
            self.settings = Settings()
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

    @staticmethod
    def ensure_restart():
        SimpleDialog("restart")

    @staticmethod
    def ensure_exit():
        SimpleDialog("quit")

    @staticmethod
    def show_info():
        SimpleDialog("info")

    def lose(self):
        self.field.show_the_bombs()
        SimpleDialog("lose")

    def win(self):
        self.field.show_the_bombs()
        SimpleDialog("win")

    def exit(self, event=None):
        self.parent.quit()

    def restart(self, event=None):
        for child in self.parent.winfo_children():
            child.destroy()
        gc.collect()
        self.__init__(self.parent, self.settings)


class Cell(tk.Button):

    def __init__(self, master, row, column):
        super().__init__(master=master)
        self.row = str(row)
        self.column = str(column)
        self.nearby_bombs = None
        self.bomb = False
        self.folder = os.path.dirname(__file__)
        self.state = "closed"
        self.closed_image = tk.PhotoImage(file=(os.path.join(self.folder, "./img/closed.png")))
        self.configure(image=self.closed_image)
        self.last_image = tk.PhotoImage(file=(os.path.join(self.folder, "./img/boom.png")))
        self.bomb_image = tk.PhotoImage(file=(os.path.join(self.folder, "./img/bomb.png")))
        self.not_bomb_image = tk.PhotoImage(file=(os.path.join(self.folder, "./img/wrong.png")))
        self.marked_image = tk.PhotoImage(file=(os.path.join(self.folder, "./img/marked.png")))
        self.opened_image = None

    # Getters
    def is_bomb(self):
        return self.bomb

    def is_closed(self):
        return self.state == "closed"

    def is_disabled(self):
        return self.state == "disabled"

    def is_marked(self):
        return self.state == "marked"

    # State changers
    def activate(self):
        self.configure(state="normal")
        self.bind("<ButtonRelease-3>", self.mark)
        self.bind("<Button-2>", self.two_buttons)
        self.bind("<ButtonRelease-2>", self.automated_opening)
        self.bind("<B2-Leave>", self.mouse_leave)
        self.bind("<B2-Motion>", self.two_buttons)

    def deactivate(self):
        self.configure(state="disabled")
        self.unbind("<ButtonRelease-3>")
        self.unbind("<Button-2>")
        self.unbind("<ButtonRelease-2>")
        self.unbind("<B2-Leave>")
        self.unbind("<B2-Motion>")

    def close(self):
        self.state = "closed"
        self.configure(image=self.closed_image, state="normal")

    def open(self):
        if not self.is_marked():
            self.configure(image=self.opened_image, relief="sunken")
            self.unbind("<B1>")
            self.state = "disabled"
            if self.is_bomb():
                self.blow_up()
                app.lose()
            elif self.nearby_bombs is None:
                self.open_zeros()

    def mark(self, event=None):
        if not self.is_disabled():
            counter = app.field.number_of_bombs
            if self.is_closed():
                self.state = "marked"
                self.configure(image=self.marked_image)
                counter.set(counter.get()-1)
            elif self.is_marked():
                self.close()
                counter.set(counter.get()+1)
            if app.field.number_of_bombs.get() == 0:
                app.field.check()

    # Other actions
    def automated_opening(self, event=None):
        neighbours = app.field.get_neighbours(self.column + self.row)
        if not (self.is_closed() or self.is_bomb()):
            amount_of_opened_nearby_bombs = 0
            for n in neighbours:
                if app.field.cells[n].is_marked():
                    amount_of_opened_nearby_bombs += 1
            if amount_of_opened_nearby_bombs == self.nearby_bombs:
                for n in neighbours:
                    cell = app.field.cells[n]
                    if cell.is_closed():
                        cell.open()
        elif self.is_closed():
            self.configure(relief="raised")
        for n in neighbours:
            cell = app.field.cells[n]
            if cell.is_closed() or cell.is_marked():
                cell.configure(relief="raised")

    def blow_up(self):
        self.configure(image=self.last_image)
        app.field.place_of_death = self.column + self.row

    # Function recursively checks if the cell has no bombs around and opens them
    def open_zeros(self):
        neighbours = app.field.get_neighbours(self.column + self.row)
        for n in neighbours:
            cell = app.field.cells[n]
            if cell.is_closed():
                cell.open()
                if cell.nearby_bombs is None:
                    cell.open_zeros()

    def two_buttons(self, event=None):
        if not self.is_marked():
            neighbours = app.field.get_neighbours(self.column + self.row)
            self.configure(relief="sunken")
            for n in neighbours:
                button = app.field.cells[n]
                if not (button.is_marked() or button.is_disabled()):
                    button.configure(relief="sunken")

    def mouse_leave(self, event=None):
        if self.is_closed():
            self.configure(relief="raised")
        neighbours = app.field.get_neighbours(self.column + self.row)
        for n in neighbours:
            button = app.field.cells[n]
            if button.is_closed():
                button.configure(relief="raised")


class DialogWindow(tk.Toplevel):

    def __init__(self):
        self.pause_the_game()
        super().__init__()
        self.resizable(0, 0)
        self.title(app.language["title"])
        self.bind("<FocusOut>", self.require_attention)
        self.content = tk.Frame(self, padx=10, pady=10)
        self.content.grid()

    @staticmethod
    def pause_the_game():
        for name in app.field.cells:
            cell = app.field.cells[name]
            cell.deactivate()

    def resume(self, event=None):
        self.destroy()
        for name in app.field.cells:
            cell = app.field.cells[name]
            cell.activate()

    def require_attention(self, event=None):
        self.bell()
        self.lift()
        self.focus_force()


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
        yes_command = app.exit if mode == "quit" else app.restart
        no_command = app.exit if (mode == "win" or mode == "lose") else self.resume
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


class SettingsDialog(DialogWindow):

    def __init__(self):
        super().__init__()
        settings = app.settings
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
        app.settings.apply_temp_settings(listbox_value)
        app.restart()

    def update_no_of_bombs_widget(self, number=None):
        settings = app.settings
        new_maximum = math.floor(settings.temp_rows.get() * settings.temp_columns.get() * 0.75)
        settings.max_no_of_bombs.set(new_maximum)
        self.content.bombs_scale.configure(to=new_maximum)


class Field(tk.Frame):

    def __init__(self, master, settings):
        super().__init__()
        self.place_of_death = None
        self.cells = {}
        self.columns = settings.available_columns[:settings.columns]
        self.rows = settings.rows
        self.number_of_bombs = tk.IntVar()
        self.number_of_bombs.set(settings.number_of_bombs)
        self.bomb_counter = tk.Label(master, textvariable=self.number_of_bombs, font="courier 15 bold", fg="red")
        self.bomb_counter.grid(column=0, columnspan=len(self.columns), row=0)
        self.grid()
        self.create_field()

    # Field creation and configuration
    def create_field(self):
        for i in range(self.rows):
            for j in self.columns:
                self.cells[j+str(i)] = Cell(self, i, j)
        counter = 0
        # Placing bombs
        while counter < self.number_of_bombs.get():
            cell = self.get_random_cell()
            if not cell.is_bomb():
                cell.bomb = True
                counter += 1
        # Filling non-bomb cells with numbers of nearby bombs
        for name in self.cells:
            cell = self.cells[name]
            if not cell.is_bomb():
                counter = 0
                neighbours = self.get_neighbours(cell.column+cell.row)
                for n in neighbours:
                    if self.cells[n].is_bomb():
                        counter += 1
                if counter == 0:
                    cell.opened_image = tk.PhotoImage(file=(os.path.join(cell.folder, "./img/empty.png")))
                else:
                    cell.nearby_bombs = counter
                    cell.opened_image = tk.PhotoImage(file=(os.path.join(cell.folder, "./img/{}.png".format(counter))))
        # Placing cells on the field
        for name in self.cells:
            cell = self.cells[name]
            cell.configure(command=cell.open, takefocus=0, width=24, height=24)
            cell.activate()
            cell.grid(column=self.columns.index(name[0]), row=(int(name[1:]) + 1))

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

    def get_random_cell(self):
        rnd = random.choice(list(self.cells.keys()))
        cell = self.cells[rnd]
        return cell

    # Checking if all the bombs marked correctly
    def check(self):
        for name in self.cells:
            cell = self.cells[name]
            if cell.is_bomb() and not cell.is_marked():
                if self.place_of_death is None:
                    cell.blow_up()
                app.lose()
                return
        app.win()

    def show_the_bombs(self):
        for name in self.cells:
            cell = self.cells[name]
            if cell.is_bomb() and not cell.is_marked() and name != self.place_of_death:
                cell.configure(image=cell.bomb_image)
            elif not cell.is_bomb() and cell.is_marked():
                cell.configure(image=cell.not_bomb_image)


class Settings(object):

    def __init__(self):
        self.version = "2.0.0rc1"
        self.rows = 10
        self.temp_rows = tk.IntVar()
        self.temp_rows.set(self.rows)
        self.columns = 10
        self.temp_columns = tk.IntVar()
        self.temp_columns.set(self.columns)
        self.number_of_bombs = 15
        self.temp_no_of_bombs = tk.IntVar()
        # I know, not all of them are used, but the whole alphabet is more beautiful
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
        self.max_no_of_bombs.set(math.floor(self.temp_rows.get() * self.temp_columns.get() * 0.75))

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


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
