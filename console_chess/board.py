from abc import ABC, abstractmethod, abstractproperty
import threading
import asyncio
import tkinter as tk
from copy import deepcopy
import sqlite3 as sql
from util import Const, override
from square import Square
from myexception import MyException

def success_add(f):
    def new_function(*args):
        print("Board created successfully")
        return f(*args)
    return new_function

class Board():
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title("Error log")
        self.__root.geometry("300x30")
        self.__error_log = tk.StringVar(value="")
        tk.Label(self.__root, textvariable=self.__error_log, foreground="red").pack()

        self.__board = [[Square(i, j) for j in range(Const.length.value + 1)] for i in range(Const.length.value + 1)]
        self.__white_king_index = [5, 1]
        self.__black_king_index = [5, 8]
        self.__move = Const.white.value
        self.__count_moves = 1
        self.__add_all()
        self.__print_board()

        self.__task = threading.Thread(target=self.display)
        self.__task.start()
        self.__root.mainloop()

    def __connect_database(self):
        self.__connection = sql.connect("chess.db")
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS Games"
                              f"(ID INTEGER PRIMARY KEY,"
                              f"winner REAL NOT NULL,"
                              f"moves TEXT NOT NULL)")
        value = self.__cursor.execute("SELECT max(id) FROM Games").fetchone()[0]
        self.__game_id = int(value) + 1 if value else 1

    def __add_record(self):
        if self.__move == Const.white.value:
            color = Const.black.value
        else:
            color = Const.white.value
        self.__cursor.execute("INSERT INTO Games VALUES(?, ?, ?)", (self.__game_id, color, self.__count_moves))
        self.__connection.commit()

    def display(self):
        self.__connect_database()
        st = input()
        while st != "Q":
            try:
                pos, new_pos = st.split("-")
                xpos, ypos = Square.alpha_to_digit(pos[0].upper()), int(pos[1])
                new_xpos, new_ypos = Square.alpha_to_digit(new_pos[0].upper()), int(new_pos[1])
                if self.__move_figure(xpos, ypos, new_xpos, new_ypos):
                    if self.__move == Const.white.value:
                        self.__move = Const.black.value
                    else:
                        self.__move = Const.white.value
                    if self.__is_checkmate(new_xpos, new_ypos):
                        self.__print_board()
                        self.__add_record()
                        print("Game over")
                        exit()
                    self.__print_board()
                    self.__error_log.set("")
                    self.__count_moves += 1
            except (ValueError, IndexError):
                self.__error_log.set('Wrong input')
            except MyException as err:
                self.__error_log.set(str(err))
            st = input()

    @success_add
    def __add_all(self):
        double_figures = list(Const.fig.value.values())[:3]
        try:
            for x in range(1, 4):
                self.__board[x][1].add_figure(double_figures[x - 1], Const.white.value)
                self.__board[Const.length.value + 1 - x][1].add_figure(double_figures[x - 1], Const.white.value)
                self.__board[x][Const.length.value].add_figure(double_figures[x - 1], Const.black.value)
                self.__board[Const.length.value + 1 - x][Const.length.value].add_figure(double_figures[x - 1], Const.black.value)
            self.__board[4][1].add_figure(Const.fig.value['Q'], Const.white.value)
            self.__board[5][1].add_figure(Const.fig.value['K'], Const.white.value)
            self.__board[4][Const.length.value].add_figure(Const.fig.value['Q'], Const.black.value)
            self.__board[5][Const.length.value].add_figure(Const.fig.value['K'], Const.black.value)
            for x in range(1, Const.length.value + 1):
                self.__board[x][2].add_figure(Const.fig.value['P'], Const.white.value)
                self.__board[x][Const.length.value - 1].add_figure(Const.fig.value['P'], Const.black.value)
        except MyException as err:
            self.__error_log.set(str(err))

    def __can_move_figure(self, xpos, ypos, new_xpos, new_ypos):
        if not Square.is_onboard(new_xpos, new_ypos):
            return 'Move cannot be done'
        dif_x, dif_y = new_xpos - xpos, new_ypos - ypos
        try:
            if self.__board[xpos][ypos].is_long_ranged():
                if dif_x and not dif_y or not dif_x and dif_y or abs(dif_x) == abs(dif_y):
                    divider = max(abs(dif_x), abs(dif_y))
                    if ((dif_x // divider * (Const.length.value - 1), dif_y // divider * (Const.length.value - 1))
                            in self.__board[xpos][ypos].get_moves()):
                        sign_x, sign_y = dif_x // divider, dif_y // divider
                        x, y = xpos, ypos
                        for i in range(1, divider):
                            x += sign_x
                            y += sign_y
                            if not self.__board[x][y].is_empty():
                                return 'Move cannot be done'
                    else:
                        return 'Move cannot be done'
                else:
                    return 'Move cannot be done'
            elif (dif_x, dif_y) not in self.__board[xpos][ypos].get_moves():
                return 'Move cannot be done'
        except MyException as err:
            return err
        return ""

    # move figure from position (xpos, ypos) to position (new_xpos, new_ypos)
    def __move_figure(self, xpos, ypos, new_xpos, new_ypos):
        try:
            if self.__board[xpos][ypos].get_color() != self.__move:
                raise MyException(f"It\'s {self.__move} move")
            res = self.__can_move_figure(xpos, ypos, new_xpos, new_ypos)
            if res:
                raise MyException(str(res))
            if self.__will_be_check(xpos, ypos, new_xpos, new_ypos):
                raise MyException('Move cannot be done')
            if self.__board[new_xpos][new_ypos].is_empty():
                self.__board[new_xpos][new_ypos].set_figure(self.__board[xpos][ypos].remove_figure())
            elif self.__board[xpos][ypos].get_color() != self.__board[new_xpos][new_ypos].get_color():
                self.__board[new_xpos][new_ypos].delete_figure()
                self.__board[new_xpos][new_ypos].set_figure(self.__board[xpos][ypos].remove_figure())
            else:
                raise MyException('Move cannot be done')
            if self.__board[new_xpos][new_ypos].is_pawn():
                self.__pawn_to_figure(new_xpos, new_ypos)
            elif self.__board[new_xpos][new_ypos].is_king():
                if self.__board[new_xpos][new_ypos].get_color() == Const.white.value:
                    self.__white_king_index = [new_xpos, new_ypos]
                else:
                    self.__black_king_index = [new_xpos, new_ypos]
        except MyException as err:
            if self.__board[xpos][ypos].is_pawn() and self.__board[xpos][ypos].get_color() == self.__move:
                dif = (new_xpos - xpos, new_ypos - ypos)
                if dif == self.__board[xpos][ypos].get_straight_move() and self.__board[new_xpos][new_ypos].is_empty() \
                        or dif == self.__board[xpos][ypos].get_big_straight_move() and \
                        self.__board[new_xpos][new_ypos].is_empty() and \
                        self.__board[(new_xpos + xpos) // 2][(new_ypos + ypos) // 2].is_empty():
                    if self.__will_be_check(xpos, ypos, new_xpos, new_ypos):
                        self.__error_log.set(str(err))
                        return False
                    self.__board[new_xpos][new_ypos].set_figure(self.__board[xpos][ypos].remove_figure())
                    self.__pawn_to_figure(new_xpos, new_ypos)
                    return True
                else:
                    self.__error_log.set(str(err))
            else:
                self.__error_log.set(str(err))
            return False
        return True

    def __is_check(self, color):
        if color == Const.white.value:
            king = self.__white_king_index
        else:
            king = self.__black_king_index
        for i in range(1, Const.length.value + 1):
            for j in range(1, Const.length.value + 1):
                square = self.__board[i][j]
                if square.is_empty():
                    continue
                if square.get_color() == color:
                    continue
                if not self.__can_move_figure(i, j, *king):
                    return True
        return False

    def __will_be_check(self, xpos, ypos, new_xpos, new_ypos):
        ans = False
        if self.__board[new_xpos][new_ypos].is_empty():
            prev = None
            self.__board[new_xpos][new_ypos].set_figure(self.__board[xpos][ypos].remove_figure())
        else:
            prev = self.__board[new_xpos][new_ypos].remove_figure()
            self.__board[new_xpos][new_ypos].set_figure(self.__board[xpos][ypos].remove_figure())
        if self.__board[new_xpos][new_ypos].is_king():
            color = self.__board[new_xpos][new_ypos].get_color()
            if color == Const.white.value:
                index = self.__white_king_index
                self.__white_king_index = [new_xpos, new_ypos]
            else:
                index = self.__black_king_index
                self.__black_king_index = [new_xpos, new_ypos]
        else:
            color = None

        if self.__is_check(self.__board[new_xpos][new_ypos].get_color()):
            ans = True
        else:
            ans = False

        if color == Const.white.value:
            self.__white_king_index = index
        elif color == Const.black.value:
            self.__black_king_index = index
        self.__board[xpos][ypos].set_figure(self.__board[new_xpos][new_ypos].remove_figure())
        if prev:
            self.__board[new_xpos][new_ypos].set_figure(prev)

        return ans

    def __is_checkmate(self, new_xpos, new_ypos):
        if not self.__is_check(self.__move):
            return False
        if self.__move == Const.white.value:
            xpos, ypos = self.__white_king_index
        else:
            xpos, ypos = self.__black_king_index
        for x, y in self.__board[xpos][ypos].get_moves():
            if not self.__can_move_figure(xpos, ypos, xpos + x, ypos + y) and not self.__will_be_check(xpos, ypos, xpos + x, ypos + y) \
                and (self.__board[xpos + x][ypos + y].is_empty() or \
                     self.__board[xpos + x][ypos + y].get_color() != self.__board[xpos][ypos].get_color()):
                return False
        color = self.__board[new_xpos][new_ypos].get_color()
        target = [(new_xpos, new_ypos)]
        if self.__board[new_xpos][new_ypos].is_long_ranged():
            dif_x, dif_y = new_xpos - xpos, new_ypos - ypos
            divider = max(abs(dif_x), abs(dif_y))
            sign_x, sign_y = dif_x // divider, dif_y // divider
            x, y = xpos, ypos
            for i in range(1, divider):
                x += sign_x
                y += sign_y
                target.append((x, y))
        for i in range(1, Const.length.value + 1):
            for j in range(1, Const.length.value + 1):
                square = self.__board[i][j]
                if square.is_empty():
                    continue
                if square.get_color() == color:
                    continue
                for x, y in target:
                    if not self.__can_move_figure(i, j, x, y) and not self.__will_be_check(i, j, x, y):
                        return False
        return True

    def __pawn_to_figure(self, new_xpos, new_ypos):
        color = self.__board[new_xpos][new_ypos].get_color()
        if self.__board[new_xpos][new_ypos].is_black_border_line() and color == Const.white.value \
                or self.__board[new_xpos][new_ypos].is_white_border_line() and color == Const.black.value:
            names = list(Const.fig.value.keys())[:4]
            st = input(f"Enter a figure's name to add {names}: ")
            while st not in names:
                st = input(f"Wrong input.\nEnter a figure's name to add from {names}: ")
            self.__board[new_xpos][new_ypos].delete_figure()
            self.__board[new_xpos][new_ypos].add_figure(Const.fig.value[st], color, True)

    # windows version
    """def __print_board(self):
        print("⚬⚬⚬" + "⚬⚬".join([Square.digit_to_alpha(x) for x in range(1, Const.length.value + 1)]) + "⚬⚬⚬")
        for ypos in range(Const.length.value, 0, -1):
            print(ypos, end=" ")
            for xpos in range(1, Const.length.value + 1):
                print(self.__board[xpos][ypos], end=" ")
            print(ypos)
        print("⚬⚬⚬" + "⚬⚬".join([Square.digit_to_alpha(x) for x in range(1, Const.length.value + 1)]) + "⚬⚬⚬")"""

    # linux version
    def __print_board(self):
        print("  " + " ".join([Square.digit_to_alpha(x) for x in range(1, Const.length.value + 1)]))
        for ypos in range(Const.length.value, 0, -1):
            print(ypos, end=" ")
            for xpos in range(1, Const.length.value + 1):
                print(self.__board[xpos][ypos], end=" ")
            print(ypos)
        print("  " + " ".join([Square.digit_to_alpha(x) for x in range(1, Const.length.value + 1)]))