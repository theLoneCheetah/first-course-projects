from util import Const, override
from figure import Figure
from myexception import MyException

class Pawn(Figure):
    def __init__(self, color):
        if color == Const.white.value:
            self.__moves = [(-1, 1), (1, 1)]
            self.__straight_move = (0, 1)
            self.__big_straight_move = (0, 2)
        else:
            self.__moves = [(-1, -1), (1, -1)]
            self.__straight_move = (0, -1)
            self.__big_straight_move = (0, -2)
        super().__init__(color, Const.fig.value["P"], False, self.__moves)

    def get_straight_move(self):
        return self.__straight_move

    def get_big_straight_move(self):
        return self.__big_straight_move