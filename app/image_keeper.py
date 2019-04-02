import os
import tkinter as tk


class ImageKeeper:

    def __init__(self):
        self.folder = os.path.dirname(__file__)
        self.closed = tk.PhotoImage(file=(os.path.join(self.folder, "../img/closed.png")))
        self.boom = tk.PhotoImage(file=(os.path.join(self.folder, "../img/boom.png")))
        self.bomb = tk.PhotoImage(file=(os.path.join(self.folder, "../img/bomb.png")))
        self.wrong = tk.PhotoImage(file=(os.path.join(self.folder, "../img/wrong.png")))
        self.marked = tk.PhotoImage(file=(os.path.join(self.folder, "../img/marked.png")))
        self.opened = {
            "0": tk.PhotoImage(file=(os.path.join(self.folder, "../img/empty.png"))),
            "1": tk.PhotoImage(file=(os.path.join(self.folder, "../img/1.png"))),
            "2": tk.PhotoImage(file=(os.path.join(self.folder, "../img/2.png"))),
            "3": tk.PhotoImage(file=(os.path.join(self.folder, "../img/3.png"))),
            "4": tk.PhotoImage(file=(os.path.join(self.folder, "../img/4.png"))),
            "5": tk.PhotoImage(file=(os.path.join(self.folder, "../img/5.png"))),
            "6": tk.PhotoImage(file=(os.path.join(self.folder, "../img/6.png"))),
            "7": tk.PhotoImage(file=(os.path.join(self.folder, "../img/7.png"))),
            "8": tk.PhotoImage(file=(os.path.join(self.folder, "../img/8.png")))
        }
