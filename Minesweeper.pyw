"""
This is my version of popular game Minesweeper. It has GUI and requires Tcl/Tk installed on your system
as well as tkinter module in your Python library (included by default in standard package for Windows).

It is the second version of the program because it has GUI while the first one was completely textual.

Now you can play the game on your job even if sysadmins deleted
all the games before you got your computer :)

If you find some typos or bugs please don't hesitate to report them.
"""
import tkinter as tk
import math
import random


class Application(tk.Frame):

    def __init__(self):
        self.root = tk.Tk()
        super().__init__()
        self.root.resizable(0, 0)
        self.root.config(menu=self.create_menu(self.root))
        self.root.title('My sap')
        self.root.protocol("WM_DELETE_WINDOW", self.ensure_exit)
        self.grid()
        self.field = Field(self.root)

    # Main menu
    def create_menu(self, root):
        m = tk.Menu(root)
        game = tk.Menu(m, tearoff=0)
        m.add_cascade(label="Игра", menu=game)
        game.add_command(label="Новая", command=self.ensure_restart)
        game.add_command(label="Выход", command=self.ensure_exit)
        about = tk.Menu(m, tearoff=0)
        m.add_cascade(label="О программе", menu=about)
        about.add_command(label="Версия", command=self.show_info)
        return m

    @staticmethod
    def ensure_restart():
        Dialog("restart")

    @staticmethod
    def ensure_exit():
        Dialog("quit")

    @staticmethod
    def lose():
        Dialog("lose")

    @staticmethod
    def win():
        Dialog("win")

    @staticmethod
    def show_info():
        Dialog("info")


class Dialog(tk.Toplevel):

    def __init__(self, mode):
        for name in app.field.buttons:
            app.field.buttons[name].configure(state="disabled")
        super().__init__()
        self.resizable(0, 0)
        self.title('My sap')
        self.content = tk.Frame(self, padx=10, pady=10)
        self.content.grid()
        text_label = {
            "win": "Поздравляем! Вы выиграли! Сыграем еще раз?",
            "lose": "К сожалению, вы проиграли. Хотите попробовать еще раз?",
            "restart": "Вы уверены, что хотите начать новую игру?",
            "quit": "Вы уверены, что хотите выйти из игры?",
            "info": "Текущая версия программы\n2.0.0a"
            }
        yes_command = self.exit if mode == "quit" else self.restart
        no_command = self.exit if (mode == "win" or mode == "lose") else self.resume
        self.protocol("WM_DELETE_WINDOW", no_command)
        message = tk.Label(self.content, text=text_label[mode], padx=10, pady=10)
        message.grid(row=0, column=0, columnspan=2)
        if mode == "info":
            self.ok_button = tk.Button(self.content, command=self.resume, text="OK", padx=10)
            self.ok_button.grid(row=1, column=0, columnspan=2)
            self.ok_button.focus_force()
            self.ok_button.bind("<Return>", self.resume)
        else:
            self.yes_button = tk.Button(self.content, command=yes_command, text="Да", padx=10)
            self.yes_button.grid(row=1, column=0)
            self.yes_button.bind("<Return>", yes_command)
            self.no_button = tk.Button(self.content, command=no_command, text="Нет", padx=8)
            self.no_button.grid(row=1, column=1)
            self.no_button.bind("<Return>", no_command)
            if mode == "win" or mode == "lose":
                self.yes_button.focus_force()
            else:
                self.no_button.focus_force()
            self.bind("<Right>", self.no_button_focus)
            self.bind("<Left>", self.yes_button_focus)

    def no_button_focus(self, event):
        self.no_button.focus_set()

    def yes_button_focus(self, event):
        self.yes_button.focus_set()

    def resume(self, event=None):
        self.withdraw()
        for name in app.field.buttons:
            if app.field.buttons[name].cget("text") == "X" or app.field.buttons[name].cget("text") == "":
                color = app.field.color_chooser(name)
                app.field.buttons[name].configure(state="normal", disabledforeground=color)

    def restart(self, event=None):
        self.withdraw()
        app.field = Field(app.root)

    def exit(self, event=None):
        self.withdraw()
        app.quit()


class Field(tk.Frame):

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.cells = {}
        self.buttons = {}
        self.columns = "abcdefghij"
        self.rows = 10
        self.number_of_bombs = 20
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
            if self.cells[j+str(i)].value != "!":
                self.cells[j+str(i)].value = "!"
                counter += 1
        # Filling non-bomb cells with numbers of nearby bombs
        for i in range(self.rows):
            for j in self.columns:
                cell = self.cells[j+str(i)]
                if cell.value != "!":
                    counter = 0
                    neighbours = self.get_neighbours(j+str(i))
                    for n in neighbours:
                        if self.cells[n].value == "!":
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
                self.buttons[name].bind("<Button-1>"+"<Button-3>", self.cells[name].two_buttons)
                self.buttons[name].bind("<ButtonRelease-1>"+"<ButtonRelease-3>", self.cells[name].automated_opening)
                self.buttons[name].bind("<Leave>", self.cells[name].mouse_leave)
                self.buttons[name].bind("<B1-Motion>"+"<B3-Motion>", self.cells[name].two_buttons)
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
            if self.cells[name].value == "!" and self.buttons[name].cget("text") == "":
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


class Cell:

    def __init__(self, row, column, value):
        self.row = str(row)
        self.column = str(column)
        self.value = str(value)

    def automated_opening(self, event):
        neighbours = app.field.get_neighbours(self.column+self.row)
        button_text = app.field.buttons[self.column+self.row].cget("text")
        if button_text != "" and button_text != "X":
            amount_of_opened_nearby_bombs = 0
            for n in neighbours:
                if app.field.buttons[n].cget("text") == "X":
                    amount_of_opened_nearby_bombs += 1
            if str(amount_of_opened_nearby_bombs) == self.value:
                for n in neighbours:
                    app.field.cells[n].open_cell()
        for n in neighbours:
            if app.field.buttons[n].cget("text") == "" or app.field.buttons[n].cget("text") == "X":
                app.field.buttons[n].configure(relief="raised")

    def open_cell(self):
        if app.field.buttons[self.column+self.row].cget("text") != "X":
            value = self.value
            if value == "!":
                app.field.buttons[self.column+self.row].configure(bg="red")
                app.lose()
            app.field.buttons[self.column+self.row].configure(text=value, state="disabled", relief="sunken")
            if value == " ":
                self.open_zeros()

    # Function recursively checks if the cell has no bombs around and opens them
    def open_zeros(self):
        neighbours = app.field.get_neighbours(self.column+self.row)
        for n in neighbours:
            if app.field.buttons[n].cget("text") == "":
                app.field.cells[n].open_cell()
                if app.field.cells[n].value == " ":
                    app.field.cells[n].open_zeros()

    def mark_cell(self, event):
        if app.field.buttons[self.column+self.row].cget("state") != "disabled":
            if app.field.buttons[self.column+self.row].cget("text") == "":
                app.field.buttons[self.column+self.row].configure(text="X", disabledforeground="black")
                app.field.number_of_bombs -= 1
            else:
                color = app.field.color_chooser(self.column+self.row)
                app.field.buttons[self.column+self.row].configure(text="", disabledforeground=color)
                app.field.number_of_bombs += 1
            app.field.bomb_counter.configure(text=app.field.number_of_bombs)
            if app.field.number_of_bombs == 0:
                app.field.check()

    def two_buttons(self, event):
        if app.field.buttons[self.column+self.row].cget("text") != "X":
            neighbours = app.field.get_neighbours(self.column+self.row)
            for n in neighbours:
                if app.field.buttons[n].cget("text") != "X":
                    app.field.buttons[n].configure(relief="sunken")

    def mouse_leave(self, event):
        neighbours = app.field.get_neighbours(self.column+self.row)
        for n in neighbours:
            if app.field.buttons[n].cget("text") == "":
                app.field.buttons[n].configure(relief="raised")
                

app = Application()
app.mainloop()
