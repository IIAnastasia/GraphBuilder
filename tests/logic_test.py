import sys
import unittest
import pandas as pd
import os

root_path = os.path.split(os.path.abspath(sys.argv[0]))[0] + "/.."
sys.path.append(root_path)

import graphs.graph
import handlers.file_handler
import handlers.graph_handler
import handlers.string_handler


class FileHandlerTester(unittest.TestCase):
    def test_file(self):
        self.assertTrue(
            pd.DataFrame([
                [1, 5], [2, 3], [3, 2], [4, 6], [5, 8], [6, 3], [7, 1], [8, 0],
                [9, 20], [10, 3]
            ]).equals(handlers.file_handler.FileHandler.
                      read_csv(root_path + "/test_files/first.csv")))


class StringParseTester(unittest.TestCase):
    def test_string(self):
        s1 = handlers.string_handler.StringParser("y = x^2",
                                                  {"x": 0.0, "y": 0.0})
        self.assertEqual(s1.check({"x": 0, "y": 0}, 0.01), True)
        self.assertEqual(s1.check({"x": 0, "y": 1}, 0.01), False)
        self.assertEqual(s1.check({"x": 0, "y": 1}, 2), True)

    def test_reload(self):
        s1 = handlers.string_handler.StringParser("y = x^2",
                                                  {"x": 0.0, "y": 0.0})
        self.assertEqual(s1.check({"x": -1, "y": 1}, 0.01), True)
        s2 = handlers.string_handler.StringParser("y = x^3",
                                                  {"x": 0.0, "y": 0.0})
        self.assertEqual(s2.check({"x": -1, "y": 1}, 0.01), False)
        s1.reload()
        self.assertEqual(s1.check({"x": -1, "y": 1}, 0.01), True)

    def test_no_reload(self):
        s1 = handlers.string_handler.StringParser("y = x^2",
                                                  {"x": 0.0, "y": 0.0})
        self.assertEqual(s1.check({"x": -1, "y": 1}, 0.01), True)
        s2 = handlers.string_handler.StringParser("y = x^3",
                                                  {"x": 0.0, "y": 0.0})
        self.assertEqual(s2.check({"x": -1, "y": 1}, 0.01), False)
        self.assertEqual(s1.check({"x": -1, "y": 1}, 0.01), False)


class GraphTester(unittest.TestCase):
    def test_empty_base(self):
        self.assertTrue(graphs.graph.Base().get_data().empty)

    def test_empty_graph(self):
        self.assertTrue(graphs.graph.Graph().get_data().empty)

    def test_file_base_init(self):
        data = pd.DataFrame([
            [0, 4], [1, 3], [2, 2], [3, 1], [4, 0]]
        )
        self.assertTrue(graphs.graph.Base(data).get_data().equals(data))

    def test_file_graph_init(self):
        data = pd.DataFrame([
            [0, 4], [1, 3], [2, 2], [3, 1], [4, 0]]
        )
        self.assertTrue(graphs.graph.FileGraph(data).get_data().equals(data))

    def test_text_graph_init(self):
        text_graph = graphs.graph.TextGraph("x + y = 5")
        text_graph.change_range(-10, 10, -10, 10)
        for (x, y) in text_graph.get_data().values:
            self.assertTrue(x + y - 5 < 0.1)

    def test_file_graph_change_range(self):
        data = pd.DataFrame([
            [0, 4], [1, 3], [2, 2], [3, 1], [4, 0]]
        )
        file_graph = graphs.graph.FileGraph(data)
        file_graph.change_range(-1, 1, -1, 1)
        self.assertTrue(graphs.graph.FileGraph(data).get_data().equals(data))

    def test_text_graph_change_range(self):
        text_graph = graphs.graph.TextGraph("x + y = 5")
        text_graph.change_range(-10, 10, -10, 10)
        text_graph.change_range(-5, 5, -5, 5)
        for (x, y) in text_graph.get_data().values:
            self.assertTrue(-5 <= x <= 5 and -5 <= y <= 5)


class GraphDataHandlerTester(unittest.TestCase):
    def init_graph_data_handler(self):
        data_handler = handlers.graph_handler.GraphDataHandler()
        data_handler.imaginary_add()
        data_handler.imaginary_add()
        data_handler.imaginary_add()
        data_handler.add_graph(graphs.graph.TextGraph("x + y = 5"), 1)
        data = pd.DataFrame([
            [0, 4], [1, 3], [2, 2], [3, 1], [4, 0]]
        )
        data_handler.add_graph(graphs.graph.FileGraph(data), 2)
        return data_handler

    def test_change_scale(self):
        graph_data_handler = self.init_graph_data_handler()
        x_min, x_max = graph_data_handler.get_x_limits()
        y_min, y_max = graph_data_handler.get_y_limits()
        graph_data_handler.change_scale(50, 10)
        delta_x = (x_max - x_min) * 0.5
        delta_y = (y_max - y_min) * 0.1
        x_max -= delta_x / 2
        x_min += delta_x / 2
        y_max -= delta_y / 2
        y_min += delta_y / 2
        self.assertEqual((x_min, x_max), graph_data_handler.get_x_limits())
        self.assertEqual((y_min, y_max), graph_data_handler.get_y_limits())
        self.assertTrue(graph_data_handler.get_data(2)[0].min() >= x_min and
                        graph_data_handler.get_data(2)[0].max() <= x_max and
                        graph_data_handler.get_data(2)[1].min() >= y_min and
                        graph_data_handler.get_data(2)[1].max() <= y_max)


class GraphExceptionTester(unittest.TestCase):
    def test_text_graph_exception(self):
        with self.assertRaises(graphs.graph.GraphException) as e:
            graphs.graph.TextGraph("y = tg(x)")
        self.assertEqual(str(e.exception), "Неверный формат. Должно быть:\n"
                                 "Переменные: x, y\n"
                                 "Операторы: +, -, *, /, ^\n"
                                 "Функции: sin(x), cos(x), tan(x), "
                                 "arcsin(x), arccos(x), arctan(x), "
                                 "abs(x), log(x), log10(x), exp(x)")
        with self.assertRaises(graphs.graph.GraphException) as e:
            graphs.graph.TextGraph("")
        self.assertEqual(str(e.exception), "Неверный формат. Должно быть:\n"
                                 "Переменные: x, y\n"
                                 "Операторы: +, -, *, /, ^\n"
                                 "Функции: sin(x), cos(x), tan(x), "
                                 "arcsin(x), arccos(x), arctan(x), "
                                 "abs(x), log(x), log10(x), exp(x)")
    def test_file_graph_exception(self):
        data = handlers.file_handler.FileHandler.read_csv(
            root_path + "/test_files/pie.csv")
        with self.assertRaises(graphs.graph.GraphException) as e:
            graphs.graph.FileGraph(data)
        self.assertEqual(str(e.exception), "Неверный формат данных. "
                "Должно быть 2 численных столбца без заголовков")

    def test_pie_exception(self):
        data = handlers.file_handler.FileHandler.read_csv(
            root_path + "/test_files/hist.csv")
        with self.assertRaises(graphs.graph.GraphException) as e:
            graphs.graph.Pie(data)
        self.assertEqual(str(e.exception),
                         "Неверный формат данных: должно быть два столбца "
                         "название-значение. Второй столбец должен состоять "
                         "из неотрицательных чисел")
        data = handlers.file_handler.FileHandler.read_csv(
            root_path + "/test_files/second.csv")
        with self.assertRaises(graphs.graph.GraphException) as e:
            graphs.graph.Pie(data)
        self.assertEqual(str(e.exception), "Неверный формат данных: должно быть два столбца "
                                 "название-значение. Второй столбец должен состоять "
                                 "из неотрицательных чисел")

    def test_bar_exception(self):
        data = handlers.file_handler.FileHandler.read_csv(
            root_path + "/test_files/hist.csv")
        with self.assertRaises(graphs.graph.GraphException) as e:
            graphs.graph.Bar(data)
        self.assertEqual(str(e.exception),
                         "Неверный формат данных. "
                "Должно быть 2 столбца без заголовков")

    def test_file_exception(self):
        file_name = root_path + "/test_files/not_csv.txt"
        with self.assertRaises(handlers.file_handler.FileException) as e:
            handlers.file_handler.FileHandler.read_csv(file_name)
        self.assertEqual(str(e.exception), f"Не удалось открыть файл {os.path.abspath(file_name)}"
                                "Проверьте, что он не пуст и в формате csv")
        file_name = root_path + "/test_files/empty.csv"
        with self.assertRaises(handlers.file_handler.FileException) as e:
            handlers.file_handler.FileHandler.read_csv(file_name)
        self.assertEqual(str(e.exception), f"Не удалось открыть файл {os.path.abspath(file_name)}"
                                "Проверьте, что он не пуст и в формате csv")



unittest.main()


