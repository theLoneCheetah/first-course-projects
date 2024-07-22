import tkinter as tk
from util import Const

class GraphicalInterface:
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title("Error log")
        self.__root.geometry("300x30")

        self.__error_log = tk.StringVar(value="ter")
        tk.Label(self.__root, textvariable=self.__error_log, foreground="red").pack()

    def start(self):
        self.__root.mainloop()

    def set_error(self, err):
        self.__error_log = err