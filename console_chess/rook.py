from util import Const, override
from figure import Figure
from myexception import MyException

class Rook(Figure):
    def __init__(self, color):
        self.__moves = [(-7, 0), (0, 7), (7, 0), (0, -7)]
        super().__init__(color, Const.fig.value["R"], True, self.__moves)