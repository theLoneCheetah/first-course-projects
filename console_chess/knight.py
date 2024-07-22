from util import Const, override
from figure import Figure
from myexception import MyException

class Knight(Figure):
    def __init__(self, color):
        self.__moves = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2)]
        super().__init__(color, Const.fig.value["Kn"], False, self.__moves)