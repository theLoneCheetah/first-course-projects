from abc import ABC, abstractmethod, abstractproperty
from util import Const, override
from figure import Figure
from myexception import MyException

class King(Figure):
    def __init__(self, color):
        self.__moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 1), (1, 0), (1, -1)]
        super().__init__(color, Const.fig.value["K"], False, self.__moves)