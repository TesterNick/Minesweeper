import os
import tkinter as tk


class ImageKeeper:

    def __init__(self):
        img = tk.PhotoImage
        join = os.path.join
        self.folder = os.path.dirname(__file__)
        self.closed = img(file=(join(self.folder, "../img/closed.png")))
        self.boom = img(file=(join(self.folder, "../img/boom.png")))
        self.bomb = img(file=(join(self.folder, "../img/bomb.png")))
        self.wrong = img(file=(join(self.folder, "../img/wrong.png")))
        self.marked = img(file=(join(self.folder, "../img/marked.png")))
        self.opened = {
            "0": img(file=(join(self.folder, "../img/empty.png"))),
            "1": img(file=(join(self.folder, "../img/1.png"))),
            "2": img(file=(join(self.folder, "../img/2.png"))),
            "3": img(file=(join(self.folder, "../img/3.png"))),
            "4": img(file=(join(self.folder, "../img/4.png"))),
            "5": img(file=(join(self.folder, "../img/5.png"))),
            "6": img(file=(join(self.folder, "../img/6.png"))),
            "7": img(file=(join(self.folder, "../img/7.png"))),
            "8": img(file=(join(self.folder, "../img/8.png")))
        }
