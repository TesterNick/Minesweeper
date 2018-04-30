import locale
import math
import tkinter as tk
from .settings_dialog import SettingsDialog


class Settings(object):

    def __init__(self, app):
        self.version = "2.0.0rc2"
        self.app = app
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

    def change_settings_dialog(self):
        SettingsDialog(self.app)

    def default_language(self):
        if locale.getdefaultlocale()[0].lower() == "ru_ru":
            return self.russian
        else:
            return self.english

    def get_field_settings(self):
        return self.available_columns[:self.columns], self.rows, self.number_of_bombs
