import tkinter as tk
from enum import Enum

class Const(Enum):
    window_width = 300
    caption_width = 80
    field_width = 180
    # windows version
    #background = 'SystemButtonFace'
    # linux version
    background = 'gray85'
    menu = ["Траты", "Пополнения", "Баланс"]
    categ = ["---", "Продукты", "ЖКХ, связь, интернет", "Образование", "Транспорт", "Погашение кредитов", "Переводы и наличные",
             "Автомобиль", "Маркетплейсы и доставка", "Товары для дома", "Одежда и обувь", "Мебель и техника",
             "Красота и здоровье", "Кафе и рестораны", "Цветы и подарки", "Отдых и развлечения", "Другое"]
    table_headings = ["ID", "Date", "Sum", "Category"]
    column_width = list(map(int, [window_width / 3 - 50, window_width / 3, window_width / 3, window_width / 3 + 50]))