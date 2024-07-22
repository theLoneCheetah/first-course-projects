from abc import ABC, abstractmethod, abstractproperty
from util import Const, override
from myexception import MyException

class Figure(ABC):
    def __init__(self, color, name=None, long_range=None, moves=None):
        self._color = color
        self._name = name
        self._long_range = long_range
        self._moves = moves

    def __add__(self, other):   # other is a string, for example, "A1" or "E4"
        self._change_position(other[0].upper(), int(other[1]))
        return self

    @property
    def get_name(self):
        return self._name

    @property
    def get_color(self):
        return self._color

    @property
    def get_long_range(self):
        return self._long_range

    def get_moves(self):
        return self._moves

    @property
    def get_name(self):
        return self._name

    def __str__(self):
        return f"{str(self._color)} {str(self._name)}"