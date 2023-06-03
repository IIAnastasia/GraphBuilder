from graphs.graph import Base, Graph, TextGraph, FileGraph
from graphs.graph_data_types import PlotType, PieType


class BaseDataHandler:
    def __init__(self):
        self.data = []

    def imaginary_add(self):
        self.data.append(Base())
        return len(self.data) - 1

    def remove_graph(self, index):
        self.data.pop(index)

    def size(self):
        return len(self.data)

    def get_data(self, index):
        return self.data[index].get_data()

    def clear(self):
        self.data = []

    def add_graph(self, graph, index):
        if index == len(self.data):
            self.data.append(graph)
        else:
            self.data[index] = graph


class GraphDataHandler(BaseDataHandler):
    def __init__(self):
        super(GraphDataHandler, self).__init__()
        self.x_real_min = -10
        self.x_real_max = 10
        self.y_real_min = -10
        self.y_real_max = 10
        self.x_min = -10
        self.x_max = 10
        self.y_min = -10
        self.y_max = 10
        self.x_delta_percent = 0
        self.y_delta_percent = 0
        self.x_length = 20
        self.y_length = 20
        self.empty = True

    def change_scale(self, x_percent, y_percent):
        # Пересчет масштаба
        if x_percent == 100:
            x_percent = 99
        if y_percent == 100:
            y_percent = 99
        delta_x = (self.x_real_max - self.x_real_min) * (
                x_percent - self.x_delta_percent) / 100
        delta_y = (self.y_real_max - self.y_real_min) * (
                y_percent - self.y_delta_percent) / 100
        self.x_max -= delta_x / 2
        self.x_min += delta_x / 2
        self.y_max -= delta_y / 2
        self.y_min += delta_y / 2
        self.x_delta_percent = x_percent
        self.y_delta_percent = y_percent
        self.update_data()

    def move(self, x_percent, y_percent):
        # Пересчет масштаба
        delta_x = (self.x_max - self.x_min) * x_percent / 100
        delta_y = (self.y_max - self.y_min) * y_percent / 100
        self.x_max += delta_x
        self.x_min += delta_x
        self.y_max += delta_y
        self.y_min += delta_y
        self.update_data()

    def update_data(self):
        # Применение изменения данных
        for i in self.data:
            i.change_range(self.x_min, self.x_max, self.y_min, self.y_max)

    def get_x_limits(self):
        return self.x_min, self.x_max

    def get_y_limits(self):
        return self.y_min, self.y_max

    def add_graph(self, graph, index):
        # Если граф текстовый, то он подстраивается под существующий масштаб
        if type(graph) == TextGraph:
            self.empty = False
            graph.change_range(self.x_min, self.x_max, self.y_min, self.y_max)

        # Если граф файловый, то он может уменьшить масштаб
        elif type(graph) == FileGraph:
            # Если первым вводится файловый граф, то меняем масштаб по
            # умолчанию на его масштаб
            if self.empty:
                self.x_real_min = graph.x_min
                self.x_real_max = graph.x_max
                self.y_real_min = graph.y_min
                self.y_real_max = graph.y_max
                self.x_max = self.x_real_max
                self.x_min = self.x_real_min
                self.y_max = self.y_real_max
                self.y_min = self.y_real_min
                self.empty = False
            elif graph.x_min < self.x_real_min or \
                    graph.x_max > self.x_real_max or \
                    graph.y_min < self.y_real_min or \
                    graph.y_max > self.y_real_max:
                self.x_real_min = min(graph.x_min, self.x_real_min)
                self.x_real_max = max(graph.x_max, self.x_real_max)
                self.y_real_min = min(graph.y_min, self.y_real_min)
                self.y_real_max = max(graph.y_max, self.y_real_max)
                self.x_max = self.x_real_max
                self.x_min = self.x_real_min
                self.y_max = self.y_real_max
                self.y_min = self.y_real_min
                self.x_delta_percent = 0
                self.y_delta_percent = 0
                self.update_data()
        super(GraphDataHandler, self).add_graph(graph, index)

    # Если есть поле для ввода графа, но граф не ввели
    def imaginary_add(self):
        self.data.append(Graph())
        return len(self.data) - 1


# Связывает ViewerHandler и DataHandler, заботится о типах
class GraphHandler:
    def __init__(self, update_immediately=True):
        self.graph_data_handler = GraphDataHandler()
        self.graph_view_handler = PlotViewHandler(
            graph_data_handler=self.graph_data_handler)
        self.graph_type = PlotType()
        self.update_immediately = update_immediately

    def add_graph(self, graph, index):
        self.graph_data_handler.add_graph(graph, index)
        self.graph_view_handler.update()

    def imaginary_add(self):
        return self.graph_data_handler.imaginary_add()


    def remove_graph(self, index):
        self.graph_data_handler.remove_graph(index)
        self.graph_view_handler.update()

    def change_scale(self, x_percent, y_percent):
        self.graph_data_handler.change_scale(x_percent, y_percent)
        if self.update_immediately:
            self.graph_view_handler.update()

    def move(self, x_percent, y_percent):
        self.graph_data_handler.move(x_percent, y_percent)
        if self.update_immediately:
            self.graph_view_handler.update()


    def change_type(self, graph_type):
        self.graph_type = graph_type
        self.graph_data_handler.clear()
        self.graph_view_handler.clear()
        if self.graph_type.is_plot():
            self.graph_data_handler = GraphDataHandler()
            self.graph_view_handler = PlotViewHandler(
                *self.graph_view_handler.get_params(),
                self.graph_data_handler, self.graph_type)
        else:
            self.graph_data_handler = BaseDataHandler()
            self.graph_view_handler = OtherViewHandler(
                *self.graph_view_handler.get_params(),
                self.graph_data_handler,
                self.graph_type)

    def download(self, destination):
        if not self.update_immediately:
            self.graph_view_handler.update()
        self.graph_view_handler.figure.savefig(destination, format="png")




# Базовая работа с отображением. Настройки canvas
class BaseViewHandler:
    def __init__(self, figure=None, subplot=None,
                 canvas=None, graph_data_handler=None, graph_type=PieType()):
        self.figure = figure
        self.subplot = subplot
        self.graph_data_handler = graph_data_handler
        self.canvas = canvas
        self.graph_type = graph_type

    def set_subplot(self, subplot):
        self.subplot = subplot

    def set_figure(self, figure):
        self.figure = figure

    def set_canvas(self, canvas):
        self.canvas = canvas

    def clear(self):
        self.figure.clf()


    def get_params(self):
        return self.figure, self.subplot, self.canvas


# Специализация для графика функции
class PlotViewHandler(BaseViewHandler):
    def __init__(self, figure=None, subplot=None,
                 canvas=None, graph_data_handler=None, graph_type=PlotType()):
        super(PlotViewHandler, self).__init__(
            figure, subplot, canvas, graph_data_handler, graph_type)

    # все графики на одном полотне, в одном масштабе
    def paint_plot(self):
        self.paint_graph(self.graph_data_handler)
        for i in range(self.graph_data_handler.size()):
            data = self.graph_data_handler.get_data(i)
            if not data.empty:
                self.subplot.plot(data[0], data[1])

    def paint_graph(self, graph_data_handler):
        self.subplot = self.figure.add_subplot(111)
        self.subplot.set(xlim=graph_data_handler.get_x_limits(),
                         ylim=graph_data_handler.get_y_limits())

    def update(self):
        self.figure.clf()
        self.paint_plot()
        if self.canvas is not None:
            self.canvas.draw()



# Специализация для остальных графиков
class OtherViewHandler(BaseViewHandler):
    def __init__(self, figure=None, subplot=None, canvas=None,
                 graph_data_handler=None,
                 graph_type=PieType()):
        super(OtherViewHandler, self).__init__(
            figure, subplot, canvas, graph_data_handler, graph_type)

    def update(self):
        # графики на разных полотнах по 2 в строке
        self.figure.clf()
        rows = (self.graph_data_handler.size() + 1) // 2
        # если график только 1, то он занимает все полотно
        cols = min(2, self.graph_data_handler.size())
        for i in range(self.graph_data_handler.size()):
            subplot = self.figure.add_subplot(rows, cols, i + 1)
            if self.graph_type.is_pie():
                subplot.pie(self.graph_data_handler.get_data(i)[1],
                            labels=self.graph_data_handler.get_data(i)[0])
            elif self.graph_type.is_bar():
                subplot.bar(self.graph_data_handler.get_data(i)[0],
                            self.graph_data_handler.get_data(i)[1]
                            )
            elif self.graph_type.is_hist():
                subplot.hist(self.graph_data_handler.get_data(i)[0])
        if self.canvas is not None:
            self.canvas.draw()
