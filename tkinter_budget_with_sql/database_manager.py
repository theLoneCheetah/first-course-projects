import sqlite3 as sql
from util import Const

class DatabaseManager:
    # connect with the database, create two tables and remember the next id for both
    def __init__(self):
        self.__connection = sql.connect("budget.db")
        self.__cursor = self.__connection.cursor()

        self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS Expenses"
                       f"({Const.table_headings.value[0]} INTEGER PRIMARY KEY,"
                       f"{Const.table_headings.value[1]} TEXT NOT NULL,"
                       f"{Const.table_headings.value[2]} REAL NOT NULL,"
                       f"{Const.table_headings.value[3]} TEXT NOT NULL)")
        value = self.__cursor.execute("SELECT max(id) FROM Expenses").fetchone()[0]
        self.__expenses_id = int(value) + 1 if value else 1

        self.__cursor.execute(f"CREATE TABLE IF NOT EXISTS Replenishments"
                              f"({Const.table_headings.value[0]} INTEGER PRIMARY KEY,"
                              f"{Const.table_headings.value[1]} TEXT NOT NULL,"
                              f"{Const.table_headings.value[2]} REAL NOT NULL)")
        value = self.__cursor.execute("SELECT max(id) FROM Replenishments").fetchone()[0]
        self.__replenishments_id = int(value) + 1 if value else 1

    # count the current balance in the start, actually when the database already exists
    def count_balance(self):
        plus = self.__cursor.execute(f"SELECT sum({Const.table_headings.value[2]}) FROM Replenishments").fetchone()[0]
        plus = float(plus) if plus else 0
        minus = self.__cursor.execute(f"SELECT sum({Const.table_headings.value[2]}) FROM Expenses").fetchone()[0]
        minus = float(minus) if minus else 0
        return plus - minus

    # return the last replenishment date
    def get_replenishment_date(self):
        return self.__cursor.execute(f"SELECT {Const.table_headings.value[1]} FROM Replenishments "
                                     f"ORDER BY {Const.table_headings.value[1]} DESC LIMIT 1").fetchone()

    # add new expense and increase id
    def insert_expense(self, date, sm, categ):
        self.__cursor.execute("INSERT INTO Expenses VALUES(?, ?, ?, ?)",
                              (self.__expenses_id, date, sm, categ))
        self.__connection.commit()
        self.__expenses_id += 1

    # add new replenishment and increase id
    def insert_replenishment(self, date, sm):
        self.__cursor.execute("INSERT INTO Replenishments VALUES(?, ?, ?)",
                              (self.__replenishments_id, date, sm))
        self.__connection.commit()
        self.__replenishments_id += 1

    # return list of records from one of the tables by given tags
    def show_data(self, table, date, categ):
        if date:
            if categ:
                self.__cursor.execute(f"SELECT * FROM {table} WHERE {Const.table_headings.value[1]}=? "
                                      f"AND {Const.table_headings.value[3]}=?", (date, categ))
            else:
                self.__cursor.execute(f"SELECT * FROM {table} "
                                      f"WHERE {Const.table_headings.value[1]}=?", (date,))
        else:
            if categ:
                self.__cursor.execute(f"SELECT * FROM {table} "
                                      f"WHERE {Const.table_headings.value[3]}=?", (categ,))
            else:
                self.__cursor.execute(f"SELECT * FROM {table}")
        return self.__cursor.fetchall()

    # count amount of money to lose/get by removing records, return with minus if it's an expense
    def count_removing_records(self, ids, table):
        loss = 0
        for id in ids:
            self.__cursor.execute(f"SELECT {Const.table_headings.value[2]} FROM {table} WHERE "
                                  f"{Const.table_headings.value[0]}=?", (id,))
            loss += self.__cursor.fetchone()[0]

        if table == "Expenses":
            return -loss
        else:
            return loss

    # remove records from one the tables by given ids
    def remove_records(self, ids, table):
        for id in ids:
            self.__cursor.execute(f"DELETE FROM {table} WHERE {Const.table_headings.value[0]}=?", (id,))
        self.__connection.commit()