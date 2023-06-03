import numpy as np
import pandas as pd

from handlers.string_handler import StringParser


class GraphException(Exception):
    pass


# Самый общий тип графиков. Просто хранит данные
class Base:
    def __init__(self, data=pd.DataFrame(columns=[0, 1])):
        self.data = data

    def get_data(self):
        return self.data


class Pie(Base):
    def __init__(self, data=pd.DataFrame(columns=[0, 1])):
        data[0] = data[0].astype({0: str})
        if (not (data.empty or
                 data.shape[1] >= 2 and
                 (data.dtypes[1] == int or data.dtypes[1] == float)
                 and all(data[1] >= 0))):
            raise GraphException(
                "Неверный формат данных: должно быть два столбца "
                "название-значение. Второй столбец должен состоять "
                "из неотрицательных чисел")
        super(Pie, self).__init__(data)


class Bar(Base):
    def __init__(self, data=pd.DataFrame(columns=[0, 1])):
        data[0] = data[0].astype({0: str})
        if not (data.empty or data.shape[1] >= 2):
            raise GraphException(
                "Неверный формат данных. "
                "Должно быть 2 столбца без заголовков")
        super(Bar, self).__init__(data)


class Hist(Base):
    def __init__(self, data=pd.DataFrame(columns=[0, 1])):
        data[0] = data[0].astype({0: str})
        super(Hist, self).__init__(data)


# Общий для графиков функций. Поддерживает изменение диапазона
class Graph(Base):
    def __init__(self, data=pd.DataFrame(columns=[0, 1])):
        super(Graph, self).__init__(data)
        if (data.shape[1] < 2 or
                not (data.empty or all(
                    [i == float or i == int for i in data.dtypes[0:2]]))):
            raise GraphException(
                "Неверный формат данных. "
                "Должно быть 2 численных столбца без заголовков")
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0

    def change_range(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max


# Файловый график
class FileGraph(Graph):
    def __init__(self, data):
        super(FileGraph, self).__init__(data)
        self.x_min = min(data[0])
        self.x_max = max(data[0])
        self.y_min = min(data[1])
        self.y_max = max(data[1])


# Текстовый график
class TextGraph(Graph):
    def __init__(self, mathString):
        super(TextGraph, self).__init__()
        try:
            self.expression = StringParser(mathString, {"x": 0.0, "y": 0.0})
        except Exception:
            raise GraphException("Неверный формат. Должно быть:\n"
                                 "Переменные: x, y\n"
                                 "Операторы: +, -, *, /, ^\n"
                                 "Функции: sin(x), cos(x), tan(x), "
                                 "arcsin(x), arccos(x), arctan(x), "
                                 "abs(x), log(x), log10(x), exp(x)",
                                 )
        self.error = 0
        self.delta_x = 0
        self.delta_y = 0

    def change_range(self, x_min, x_max, y_min, y_max):
        points_number_x = 200
        points_number_y = 200
        delta_x = (x_max - x_min) / points_number_x
        delta_y = (y_max - y_min) / points_number_y
        error = (delta_x * delta_x + delta_y * delta_y) ** 0.5 / 2
        self.expression.reload()
        current_index = 0
        arr = []
        for x in np.arange(x_min, x_max + delta_x,
                           delta_x):
            while current_index < len(self.data[0]) and \
                    self.data[0][current_index] < x:
                current_index += 1
            min_possible_y = y_min
            max_possible_y = y_max
            if current_index < len(self.data[0]):
                previous_min = y_min
                previous_max = y_max
                if current_index != 0:
                    previous_min = self.data[1][
                                       current_index - 1] - self.delta_y
                    previous_max = self.data[1][
                                       current_index - 1] + self.delta_y
                min_possible_y = min(self.data[1][current_index] - self.delta_y,
                                     previous_min)
                max_possible_y = max(self.data[1][current_index] + self.delta_y,
                                     previous_max)
            if min_possible_y < y_min - error or max_possible_y > y_max + error:
                continue
            for y in np.arange(min_possible_y, max_possible_y,
                               delta_y):
                if (self.expression.check({"x": x, "y": y},
                                          error)):
                    arr.append([x, y])
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.data = pd.DataFrame(arr)
        super(TextGraph, self).change_range(x_min, x_max, y_min, y_max)

