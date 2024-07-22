from abc import ABC, abstractmethod, abstractproperty
from util import Const, override
from figure import Figure
from king import King
from queen import Queen
from rook import Rook
from knight import Knight
from bishop import Bishop
from pawn import Pawn
from myexception import MyException

class Player():
    def __init__(self, color):
        self.__color = color
        if self.__color == "white":
            ypos = 1
        else:
            ypos = 8
        self.__king = King(ypos)
        self.__figures = []
        for i in range(2):
            self.__figures.append(Rook(8 ** i, ypos))
            self.__figures.append(Knight(8 ** i, ypos))
            self.__figures.append(Bishop(8 ** i, ypos))
        self.__figures.append(Queen(ypos))
        self.__pawns = [Pawn(i, ypos) for i in range(Const.length.value)]
        self.__all = self.__figures + self.__pawns + [self.__king]

    @property
    def color(self):
        return self.__color

    def get_figures(self):
        return sorted(self.__all, key=lambda x: [x._ypos, x._xpos])

    def print_figures(self):
        print("Цвет:", self.__color)
        self.__king.get_position()
        for i in self.__figures:
            i.get_position()
        for i in self.__pawns:
            i.get_position()