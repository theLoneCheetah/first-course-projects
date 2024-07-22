class MyException(Exception):
    def __init__(self, text):
        self.__text = text

    # return just a short string about an error occured to display on the widget
    def __str__(self):
        return self.__text