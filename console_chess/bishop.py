from util import Const, override
from figure import Figure
from myexception import MyException

class Bishop(Figure):
    def __init__(self, color):
        self.__moves = [(-7, -7), (-7, 7), (7, 7), (7, -7)]
        super().__init__(color, Const.fig.value["B"], True, self.__moves)