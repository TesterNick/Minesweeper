#!/usr/bin/env python3

"""
This is my version of popular game Minesweeper. It has GUI and requires Tcl/Tk installed on your system
as well as tkinter module in your Python library (included by default in standard package for Windows).

It is the second version of the program because it has GUI while the first one was completely textual.

Now you can play the game on your job even if sysadmins deleted
all the games before you got your computer :)

If you find some typos or bugs please don't hesitate to report them.
"""

import tkinter as tk
from app.application import Application


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
