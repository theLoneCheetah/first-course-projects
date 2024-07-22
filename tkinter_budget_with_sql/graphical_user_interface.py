import tkinter as tk
from tkinter import ttk
from datetime import datetime
from main_handler import MainHandler
from util import Const

class GraphicalUserInterface:
    # create the handler, the widget, main fields and set the default expenses mode
    # exit only if system exit occured while initialisation the handler
    def __init__(self):
        try:
            self.__handler = MainHandler()
        except SystemExit:
            exit()
        self.__root = tk.Tk()
        self.__root.title("Учёт собственных денежных средств")
        self.__root.geometry(f"{Const.window_width.value*2}x{Const.window_width.value}")

        self.__menu_field()
        self.__error_field()
        self.__make_list_frame()
        self.__replenishments_frame = tk.Frame(self.__root)
        self.__balance_frame = tk.Frame(self.__root)
        self.__make_expenses_design()

        self.__root.mainloop()

    # create the main menu with modes: expenses, replenishments and balance
    def __menu_field(self):
        self.__main_caption = tk.Label(self.__root, text="Режим")
        self.__main_caption.place(x=0, y=4, width=Const.caption_width.value)

        self.__menu_input = tk.StringVar()
        self.__menu_input.set(Const.menu.value[0])
        self.__menu_drop = tk.OptionMenu(self.__root, self.__menu_input, *Const.menu.value,
                                         command=self.__change_diaplay)
        self.__menu_drop.place(x=Const.caption_width.value-2, y=0, width=Const.field_width.value+4)

    # change mode when new was choosed in the main menu
    def __change_diaplay(self, cur):
        if cur == Const.menu.value[0]:
            self.__make_expenses_design()
        elif cur == Const.menu.value[1]:
            self.__make_replenishments_design()
        else:
            self.__make_balance_design()

    # string containing erros that may occur, with red text color, by default is empty
    def __error_field(self):
        self.__error_log = tk.StringVar()
        self.__error_log.set("")
        self.__error_output = tk.Label(self.__root, textvariable=self.__error_log,
                                       background=Const.background.value, foreground="red")
        self.__error_output.place(x=0, y=33, width=Const.window_width.value)

    # string with the date entry, frame argument relates to the frame currently in use: expenses or replenishments
    def __date_field(self, frame):
        self.__date_caption = tk.Label(frame, text="Дата")
        self.__date_caption.place(x=0, y=0, width=Const.caption_width.value)

        self.__date_input = tk.Entry(frame)
        self.__date_input.place(x=Const.caption_width.value, y=0, width=Const.field_width.value)

    # string with the sum entry, frame argument relates to the frame currently in use: expenses or replenishments
    def __sum_field(self, frame):
        self.__sum_caption = tk.Label(frame, text="Сумма")
        self.__sum_caption.place(x=0, y=20, width=Const.caption_width.value)

        self.__sum_input = tk.Entry(frame)
        self.__sum_input.place(x=Const.caption_width.value, y=20, width=Const.field_width.value)

    # string with the category entry, only for expenses
    def __category_field(self):
        self.__categ_caption = tk.Label(self.__expenses_frame, text="Категория")
        self.__categ_caption.place(x=0, y=40, width=Const.caption_width.value)

        self.__categ_input = tk.StringVar()
        self.__categ_input.set(Const.categ.value[0])
        self.__categ_drop = tk.OptionMenu(self.__expenses_frame, self.__categ_input, *Const.categ.value)
        self.__categ_drop.place(x=Const.caption_width.value-2, y=40, width=Const.field_width.value+4)

    # insert info about a new expense through the handler, set a new error that can occur in the process
    def __insert_expense(self):
        self.__error_log.set(self.__handler.check_insert_expense(self.__date_input.get(), self.__sum_input.get(),
                                                                 self.__categ_input.get()))

    # button to insert expenses
    def __add_expense(self):
        self.__add_expense_button = tk.Button(self.__expenses_frame, text="Добавить траты",
                                              command=self.__insert_expense)
        self.__add_expense_button.place(x=Const.caption_width.value+20, y=80, width=120)

    # find expenses with specified date and/or category, set a new error or show the result table
    def __find_expenses(self):
        result = self.__handler.check_show_expenses(self.__date_input.get(), self.__sum_input.get(),
                                                    self.__categ_input.get())
        if type(result) == list:
            self.__error_log.set("")
            self.__show_list(Const.table_headings.value, result)
        else:
            self.__error_log.set(result)

    # button to find expenses based on the date and/or category
    def __show_expenses(self):
        self.__view_expenses_button = tk.Button(self.__expenses_frame, text="Показать траты",
                                                command=self.__find_expenses)
        self.__view_expenses_button.place(x=Const.caption_width.value+20, y=110, width=120)

    # insert info about a new replenishment through the handler, set a new error that can occur in the process
    def __insert_replenishment(self):
        self.__error_log.set(self.__handler.check_insert_replenishment(self.__date_input.get(), self.__sum_input.get()))

    # button to insert replenishments
    def __add_replenishment(self):
        self.__add_replenishment_button = tk.Button(self.__replenishments_frame, text="Внести деньги",
                                                    command=self.__insert_replenishment)
        self.__add_replenishment_button.place(x=Const.caption_width.value+20, y=80, width=120)

    # find replenishments with specified date, set a new error or show the result table
    def __find_replenishments(self):
        result = self.__handler.check_show_replenishments(self.__date_input.get(), self.__sum_input.get())
        if type(result) == list:
            self.__error_log.set("")
            self.__show_list(Const.table_headings.value[:3], result)
        else:
            self.__error_log.set(result)

    # button to find replenishments based on the date
    def __show_replenishments(self):
        self.__view_replenishments_button = tk.Button(self.__replenishments_frame, text="Показать пополнения",
                                                      command=self.__find_replenishments)
        self.__view_replenishments_button.place(x=Const.caption_width.value+5, y=110, width=160)

    # string showing current balance based on all expenses and replenishments
    def __balance_field(self):
        self.__balance_caption = tk.Label(self.__balance_frame, text="Баланс")
        self.__balance_caption.place(x=0, y=0, width=Const.caption_width.value)

        self.__balance_output = tk.Label(self.__balance_frame, text=self.__handler.get_balance())
        self.__balance_output.place(x=Const.caption_width.value-15, y=0, width=Const.field_width.value)

    # clear current error log and table of records from the database when mode is switched
    def __clear_errors_and_list(self):
        self.__error_log.set("")
        self.__tree.delete(*self.__tree.get_children())
        self.__tree["columns"] = []

    # create the frame containing expenses mode objects
    def __make_expenses_design(self):
        self.__replenishments_frame.place_forget()
        self.__balance_frame.place_forget()
        self.__clear_errors_and_list()

        self.__expenses_frame = tk.Frame(self.__root)
        self.__expenses_frame.place(x=0, y=60, width=Const.window_width.value, height=Const.window_width.value-100)
        self.__date_field(self.__expenses_frame)
        self.__sum_field(self.__expenses_frame)
        self.__category_field()
        self.__add_expense()
        self.__show_expenses()

    # create the frame containing replenishments mode objects
    def __make_replenishments_design(self):
        self.__expenses_frame.place_forget()
        self.__balance_frame.place_forget()
        self.__clear_errors_and_list()

        self.__replenishments_frame = tk.Frame(self.__root)
        self.__replenishments_frame.place(x=0, y=60, width=Const.window_width.value,
                                                    height=Const.window_width.value - 100)
        self.__date_field(self.__replenishments_frame)
        self.__sum_field(self.__replenishments_frame)
        self.__add_replenishment()
        self.__show_replenishments()

    # create the frame containing balance mode objects
    def __make_balance_design(self):
        self.__expenses_frame.place_forget()
        self.__replenishments_frame.place_forget()
        self.__clear_errors_and_list()

        self.__balance_frame = tk.Frame(self.__root)
        self.__balance_frame.place(x=0, y=60, width=Const.window_width.value, height=Const.window_width.value-100)
        self.__balance_field()

    # create an empty table for database records with a caption and two scrollbars
    def __list_environment(self):
        self.__list_caption = tk.Label(self.__list_frame, text="Вывод записей")
        self.__list_caption.place(x=0, y=5, width=Const.window_width.value-20)

        self.__tree = ttk.Treeview(self.__list_frame)
        self.__tree.place(x=0, y=30, width=Const.window_width.value-20, height=Const.window_width.value-50)
        self.__tree["show"] = "headings"   # hide an empty first column shown by default

        self.__x_scrollbar = ttk.Scrollbar(self.__list_frame, orient="horizontal", command=self.__tree.xview)
        self.__y_scrollbar = ttk.Scrollbar(self.__list_frame, orient="vertical", command=self.__tree.yview)
        self.__x_scrollbar.place(x=0, y=Const.window_width.value-20, width=Const.window_width.value-20)
        self.__y_scrollbar.place(x=Const.window_width.value-20, y=30, height=Const.window_width.value-50)
        self.__tree.configure(xscrollcommand=self.__x_scrollbar.set, yscrollcommand=self.__y_scrollbar.set)

    # remove selected records, option means the current frame and accordingly the database table
    def __find_and_remove_records(self, table):
        result = self.__handler.check_remove_records([self.__tree.set(i, Const.table_headings.value[0])
                                                      for i in self.__tree.selection()], table)
        if result:
            self.__error_log.set(result)
        elif table == "Expenses":
            self.__find_expenses()
        else:
            self.__find_replenishments()

    # enable button to delete records, different for each mode
    def __delete_records(self, event):
        if self.__menu_input.get() == Const.menu.value[0]:   # if current mode is expenses
            self.__delete_records_button = tk.Button(self.__expenses_frame, text="Удалить траты",
                                                command=lambda table="Expenses": self.__find_and_remove_records(table))
            self.__delete_records_button.place(x=Const.caption_width.value+20, y=140, width=100)
        else:   # if current mode is replenishments
            self.__delete_records_button = tk.Button(self.__replenishments_frame, text="Удалить пополнения",
                                            command=lambda table="Replenishments": self.__find_and_remove_records(table))
            self.__delete_records_button.place(x=Const.caption_width.value+5, y=140, width=130)

    # sort table by the given column in ascending/descending orde and renew its heading to correct the lambda function
    def __sort_list(self, head, descending):
        data = sorted([(self.__tree.set(ind, head), ind) for ind in self.__tree.get_children()], reverse=descending)
        for i, elem in enumerate(data):
            self.__tree.move(elem[1], "", i)

        self.__tree.heading(head, command=lambda col=head: self.__sort_list(col, not descending))

    # display database records got from search functions, with sorting by any column by pressing on a heading
    def __show_list(self, headings, data):
        self.__tree.delete(*self.__tree.get_children())
        self.__tree["columns"] = headings   # remember the number of columns
        for i, head in enumerate(headings):
            self.__tree.column(head, width=Const.column_width.value[i])
            self.__tree.heading(head, text=head, anchor="w", command=lambda col=head: self.__sort_list(col, False))
        for line in data:
            self.__tree.insert("", "end", values=line)
        self.__tree.bind("<<TreeviewSelect>>", self.__delete_records)

    # create the frame that displays database records
    def __make_list_frame(self):
        self.__list_frame = tk.Frame(self.__root)
        self.__list_frame.place(x=Const.window_width.value, y=0, width=Const.window_width.value,
                                                                height=Const.window_width.value)
        self.__list_environment()

gui = GraphicalUserInterface()