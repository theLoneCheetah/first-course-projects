import tkinter as tk
from tkinter import messagebox

menu = ["Файл", "Операции", "Справка"]
help = """Выбор режима работы (Калькулятор/Прямоугольник) осуществляется спомощью верхнего переключателя.\n
Вводите числа в поля аргументов. При необходимости поменять аргументы местами нажмите \"Поменять местами\", для очистки полей ввода нажмите \"Очистить данные\".\n
Для выбора необходимых операций и расчётов нажмите на соответствующие галочки ниже ввода аргументов или в меню \"Операции\". Для выполнения вычислений нажмите \"Вычислить\".\n
Будьте внимательны при вводе данных. Допускаются только числа с возможной дробной частью, отделённой точкой.\n
В режиме \"Прямоугольник\" при расчёте также выполняется визуализация заданного прямоугольника. Стороны прямоугольника должны быть строго положительными."""
modes = ["Калькулятор", "Прямоугольник"]
oper = ["+", "-", "*", "/"]
oper_names = ["Сложить", "Вычесть", "Умножить", "Поделить"]
rect_oper_names = ["Периметр", "Площадь"]

class Window():
    def __init__(self):
        self.__root = tk.Tk()
        self.__root.title("Калькулятор")

        self.__create_main_modes()
        self.__rect_frame = tk.Frame(self.__root)
        self.__picture = tk.Canvas(self.__root, bg="white", width=self.__root.winfo_width() * 0.9, height=self.__root.winfo_height() * 0.9)
        self.__create_calc_frame()

        self.__root.mainloop()

    def __create_main_menu(self, frame):
        self.__main_menu = tk.Menu(self.__root, tearoff=0)

        self.__file_menu = tk.Menu(self.__root, tearoff=0)
        self.__file_menu.add_cascade(label="Выход", command=self.__root.destroy)

        self.__oper_menu = tk.Menu(self.__root, tearoff=0)
        self.__oper_menu.add_cascade(label="Очистить данные", command=self.__clear_args)
        if frame == self.__calc_frame:
            for i in range(4):
                self.__oper_menu.add_checkbutton(label=oper_names[i], variable=self.__calc_oper[i])
        else:
            for i in range(2):
                self.__oper_menu.add_checkbutton(label=rect_oper_names[i], variable=self.__rect_oper[i])

        self.__main_menu.add_cascade(label=menu[0], menu=self.__file_menu)
        self.__main_menu.add_cascade(label=menu[1], menu=self.__oper_menu)
        self.__main_menu.add_cascade(label=menu[2], command=self.__open_help)

        self.__root.config(menu=self.__main_menu)

    def __open_help(self):
        messagebox.showinfo(title=menu[2], message=help)

    def __create_main_modes(self):
        tk.Label(text="Режим:").grid(row=0, column=0)
        self.__mode_var = tk.StringVar(value=modes[0])
        tk.Radiobutton(self.__root, text=modes[0], value=modes[0], variable=self.__mode_var,
                       command=self.__switch_mode).grid(row=0, column=1)
        tk.Radiobutton(self.__root, text=modes[1], value=modes[1], variable=self.__mode_var,
                       command=self.__switch_mode).grid(row=0, column=2)

        tk.Button(self.__root, text="Выход", command=self.__root.destroy).grid(row=1, column=0, columnspan=3)

        self.__error = tk.StringVar()
        tk.Label(self.__root, textvariable=self.__error, foreground="red").grid(row=2, column=0, columnspan=3)

    def __switch_mode(self):
        if self.__mode_var.get() == modes[0]:
            self.__create_calc_frame()
        else:
            self.__create_rect_frame()

    def __switch_args(self, frame):
        x = self.__arg1.get()
        self.__arg1.set(self.__arg2.get())
        self.__arg2.set(x)
        if frame == self.__calc_frame:
            for i in range(4):
                self.__calc_results[i].set("")
        else:
            for i in range(2):
                self.__rect_results[i].set("")

    def __clear_args(self):
        self.__error.set("")
        self.__arg1.set("")
        self.__arg2.set("")

    def __main_buttons(self, frame):
        tk.Button(frame, text="Очистить данные", command=self.__clear_args).grid(row=2, column=1, columnspan=2)
        tk.Button(frame, text="Поменять местами", command=lambda f=frame: self.__switch_args(frame)).grid(row=3, column=1, columnspan=2)
        if frame == self.__calc_frame:
            tk.Button(frame, text="Вычислить", command=self.__calc_operate).grid(row=4, column=1, columnspan=2)
        else:
            tk.Button(frame, text="Вычислить", command=self.__rect_operate).grid(row=4, column=1, columnspan=2)

    def __make_entries(self, frame):
        tk.Label(frame, text="Аргументы:").grid(row=2, column=0)
        self.__arg1 = tk.StringVar()
        tk.Entry(frame, textvariable=self.__arg1).grid(row=3, column=0)
        self.__arg2 = tk.StringVar()
        tk.Entry(frame, textvariable=self.__arg2).grid(row=4, column=0)

    def __calc_operate(self):
        self.__error.set("")
        state = False
        for i in range(4):
            if not self.__calc_oper[i].get():
                self.__calc_results[i].set("")
            else:
                state = True
                try:
                    self.__calc_results[i].set(round(eval(self.__arg1.get() + oper[i] + self.__arg2.get()), 2))
                except SyntaxError:
                    self.__calc_results[i].set("")
                    self.__error.set("Неверный ввод")
                except ZeroDivisionError:
                    self.__calc_results[i].set("")
                    self.__error.set("Деление на ноль")
        if not state:
            self.__error.set("Не выбран оператор")

    def __rect_operate(self):
        try:
            a, b = float(self.__arg1.get()), float(self.__arg2.get())
            if a <= 0 or b <= 0:
                raise ZeroDivisionError
        except ValueError:
            self.__error.set("Неверный ввод")
            for i in range(2):
                self.__rect_results[i].set("")
            return
        except ZeroDivisionError:
            self.__error.set("Стороны должны быть больше нуля")
            return
        self.__error.set("")
        state = False
        for i in range(2):
            if not self.__rect_oper[i].get():
                self.__rect_results[i].set("")
            else:
                state = True
                if i == 0:
                    self.__rect_results[i].set(round((a + b) * 2, 2))
                else:
                    self.__rect_results[i].set(round(a * b, 2))
        if state:
            self.__draw_rectangle(a, b)
        else:
            self.__error.set("Не выбран оператор")

    def __draw_rectangle(self, a, b):
        k = min((self.__picture_size[0] - 20) / a, (self.__picture_size[1] - 20) / b)   # растянуть до границ
        self.__picture.delete("all")
        self.__picture.create_rectangle(10, 10, 10 + a * k, 10 + b * k, fill="lightblue")

    def __make_calc_flags(self):
        self.__calc_oper = [tk.IntVar() for i in range(4)]
        for i in range(4):
            tk.Checkbutton(self.__calc_frame, text=oper_names[i], variable=self.__calc_oper[i]).grid(row=5 + i, column=0, sticky="w")

    def __make_calc_results(self):
        self.__calc_results = [tk.StringVar() for i in range(4)]
        for i in range(4):
            tk.Label(self.__calc_frame, textvariable=self.__calc_results[i]).grid(row=5+i, column=1, sticky="e")

    def __make_rect_flags(self):
        self.__rect_oper = [tk.IntVar() for i in range(2)]
        for i in range(2):
            tk.Checkbutton(self.__rect_frame, text=rect_oper_names[i], variable=self.__rect_oper[i]).grid(row=5 + i, column=0, sticky="w")

    def __make_rect_results(self):
        self.__rect_results = [tk.StringVar() for i in range(2)]
        for i in range(2):
            tk.Label(self.__rect_frame, textvariable=self.__rect_results[i]).grid(row=5+i, column=1, sticky="e")

    def __create_calc_frame(self):
        self.__rect_frame.grid_remove()
        self.__picture.grid_remove()
        self.__calc_frame = tk.Frame(self.__root)
        self.__calc_frame.grid(row=3, column=0, columnspan=3)

        self.__make_entries(self.__calc_frame)
        self.__main_buttons(self.__calc_frame)
        self.__make_calc_results()
        self.__make_calc_flags()
        self.__create_main_menu(self.__calc_frame)
        self.__clear_args()

    def __create_rect_frame(self):
        self.__calc_frame.grid_remove()
        self.__rect_frame = tk.Frame(self.__root)
        self.__rect_frame.grid(row=3, column=0, columnspan=3)

        self.__make_entries(self.__rect_frame)
        self.__main_buttons(self.__rect_frame)
        self.__make_rect_results()
        self.__make_rect_flags()
        self.__create_main_menu(self.__rect_frame)
        self.__clear_args()

        self.__picture_size = [self.__root.winfo_width() * 0.9, self.__root.winfo_height() * 0.9]
        self.__picture = tk.Canvas(self.__root, bg="white", width=self.__picture_size[0], height=self.__picture_size[1])
        self.__picture.grid(row=4, column=0, columnspan=3)

window = Window()