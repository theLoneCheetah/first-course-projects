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

class Square():
    def __init__(self, xpos, ypos, figure = None):
        self.__xpos = xpos
        self.__ypos = ypos
        self.__figure = figure

    @staticmethod
    # check if a square is on the board (is necessary from the outer class)
    def is_onboard(xpos, ypos):
        if 1 <= xpos <= Const.length.value and 1 <= ypos <= Const.length.value:
            return True
        return False

    # check if this square is on a border line (1 or 8), by default dif equal  0, dif = 1 for pawns
    def is_white_border_line(self, dif=0):
        return self.__ypos - dif == 1

    # check if this square is on a border line (1 or 8), by default dif equal  0, dif = 1 for pawns
    def is_black_border_line(self, dif=0):
        return self.__ypos + dif == Const.length.value

    def is_empty(self):
        if self.__figure == None:
            return True
        return False

    def get_color(self):
        if self.is_empty():
            raise MyException('Square is empty')
        return self.__figure._color

    def is_king(self):
        if self.is_empty():
            raise MyException('Square is empty')
        return True if self.__figure._name == Const.fig.value['K'] else False

    def is_pawn(self):
        if self.is_empty():
            raise MyException('Square is empty')
        return True if self.__figure._name == Const.fig.value['P'] else False

    def is_long_ranged(self):
        if self.is_empty():
            raise MyException('Square is empty')
        return self.__figure._long_range

    # add new figure to the board when the game is starting
    def add_figure(self, figure, color, pawn_on_border=None):
        if not self.is_empty():
            raise MyException('Square is not empty')

        if pawn_on_border:
            if figure == Const.fig.value["Q"]:
                self.__figure = Queen(color)
                return
            elif figure == Const.fig.value["R"]:
                self.__figure = Rook(color)
                return
            elif figure == Const.fig.value["Kn"]:
                self.__figure = Knight(color)
                return
            elif figure == Const.fig.value["B"]:
                self.__figure = Bishop(color)
                return
            raise MyException('This figure cannot be placed here')

        if color == Const.white.value:
            check_fun = self.is_white_border_line
        else:
            check_fun = self.is_black_border_line

        if figure == Const.fig.value["P"]:
            if check_fun(1):
                self.__figure = Pawn(color)
                return
        elif check_fun():
            if figure == Const.fig.value["K"] and self.__xpos == 5:
                self.__figure = King(color)
                return
            elif figure == Const.fig.value["Q"] and self.__xpos == 4:
                self.__figure = Queen(color)
                return
            elif figure == Const.fig.value["R"] and (self.__xpos == 1 or self.__xpos == 8):
                self.__figure = Rook(color)
                return
            elif figure == Const.fig.value["Kn"] and (self.__xpos == 2 or self.__xpos == 7):
                self.__figure = Knight(color)
                return
            elif figure == Const.fig.value["B"] and (self.__xpos == 3 or self.__xpos == 6):
                self.__figure = Bishop(color)
                return
        raise MyException('This figure cannot be placed here')

    # get all possibles moves and directions for its figure
    def get_moves(self):
        if self.is_empty():
            raise MyException('Square is empty')
        return self.__figure.get_moves()

    # get simple straight move for a pawn without being able to take an opponent's figure
    def get_straight_move(self):
        if self.is_empty():
            raise MyException('Square is empty')
        if self.__figure._name != Const.fig.value['P']:
            raise MyException('This is not a pawn')
        return self.__figure.get_straight_move()

    # get big straight move for a pawn without being able to take an opponent's figure
    def get_big_straight_move(self):
        if self.is_empty():
            raise MyException('Square is empty')
        if self.__figure._name != Const.fig.value['P']:
            raise MyException('This is not a pawn')
        return self.__figure.get_big_straight_move()

    # set figure on this square from another position
    def set_figure(self, figure):
        if not self.is_empty():
            raise MyException('Square is not empty')
        self.__figure = figure

    # remove figure to set it on another position, after this self.delete_figure() should be called
    def remove_figure(self):
        if self.is_empty():
            raise MyException('Square is empty')
        try:
            return self.__figure
        finally:
            self.__figure = None

    # delete figure instantly, for example, when it was taken by the opponent's figure
    def delete_figure(self):
        if self.is_empty():
            raise MyException('Square is empty')
        self.__figure = None

    @staticmethod
    def alpha_to_digit(xpos):
        return ord(xpos) - Const.A.value + 1

    @staticmethod
    def digit_to_alpha(xpos):
        return chr(Const.A.value + xpos - 1)

    def __str__(self):
        if self.is_empty():
            return Const.sym.value["empty"]
        return Const.sym.value[self.__figure._color + self.__figure._name]

    def __repr__(self):
        return f"X: {Square.digit_to_alpha(self.__xpos)}, Y: {self.__ypos}, {str(self.__figure)}"