from datetime import datetime
import sys
from util import Const
from my_exception import MyException
from database_manager import DatabaseManager

class MainHandler():
    # create database manager, get current balance and the last replenishment date from it
    # raise system exit error if problems occured while connecting with the database
    def __init__(self):
        try:
            self.__database = DatabaseManager()
        except Exception as err:
            print(err)
            sys.exit()
        self.__balance = self.__database.count_balance()   # the balance can't be negative
        value = self.__database.get_replenishment_date()
        self.__replenishment_date = datetime.strptime(value[0], "%Y-%m-%d").date() if value else None

    # return the balance to show in the balance mode
    def get_balance(self):
        return self.__balance

    # check if a given date is correct, return an error or the date
    def __check_date(self, date):
        try:
            date = datetime.strptime(date, "%d.%m.%Y").date()
            if datetime.now().date() < date:
                raise MyException("Неверная дата")
        except ValueError:
            raise MyException("Дата не соответствует формату \'дд.мм.гггг\'")
        except MyException as err:
            raise err
        return date

    # check if a given sum is correct, return an error or the sum
    def __check_sum(self, sm):
        try:
            sm = float(sm)
            if sm <= 0:
                raise MyException("Сумма должна быть больше нуля")
        except ValueError:
            raise MyException("Неверно введённая сумма")
        except MyException as err:
            raise err
        return sm

    # check if given category is correct, raise an error or not
    def __check_category(self, categ):
        try:
            if categ == Const.categ.value[0]:
                raise MyException("Не выбрана категория")
        except MyException as err:
            raise err

    # check expense data accuracy and command to insert it into the database, return an error or nothing
    def check_insert_expense(self, date, sm, categ):
        try:
            date = self.__check_date(date)
            sm = self.__check_sum(sm)
            if sm > self.__balance:
                raise MyException("Недостаточно средств")
            self.__check_category(categ)
        except MyException as err:
            return err

        self.__database.insert_expense(date, sm, categ)
        self.__balance -= sm
        return ""

    # check replenishment data accuracy and command to insert it into the database, return an error or nothing
    def check_insert_replenishment(self, date, sm):
        try:
            date = self.__check_date(date)
            if self.__replenishment_date and self.__replenishment_date >= date:
                raise MyException("Неверная дата")
            if self.__replenishment_date and self.__replenishment_date.day != date.day:
                raise MyException("Поступления происходят строго раз в месяц")
            sm = self.__check_sum(sm)
        except MyException as err:
            return err

        self.__database.insert_replenishment(date, sm)
        self.__replenishment_date = date
        self.__balance += sm
        return ""

    # check expenses tags accuracy and command to find it in the database, return an error or a result
    def check_show_expenses(self, date=None, sm=None, categ=None):
        try:
            if sm:
                raise MyException("Траты не выводятся по сумме")
            if date:
                date = self.__check_date(date)
        except MyException as err:
            return err

        if categ == Const.categ.value[0]:
            categ = None

        return self.__database.show_data("Expenses", date, categ)

    # check replenishments tags accuracy and command to find it in the database, return an error or a result
    def check_show_replenishments(self, date=None, sm=None):
        try:
            if sm:
                raise MyException("Пополнения не выводятся по сумме")
            if date:
                date = self.__check_date(date)
        except MyException as err:
            return err

        return self.__database.show_data("Replenishments", date, None)

    # check amount of money by records to be deleted id and command to remove it from the database, return an error or nothing
    def check_remove_records(self, ids, table):
        try:
            if not ids:
                raise MyException("Записи не выбраны")
            loss = self.__database.count_removing_records(ids, table)
            if loss > self.__balance:
                raise MyException("Недостаточно средств")
            self.__balance -= loss
        except MyException as err:
            return err

        self.__database.remove_records(ids, table)
        return ""