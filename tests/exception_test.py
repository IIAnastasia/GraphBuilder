import os
import sys
import unittest

root_path = os.path.split(os.path.abspath(sys.argv[0]))[0] + "/.."
sys.path.append(root_path)

import graphs.graph
import handlers.file_handler
import handlers.graph_handler
import handlers.string_handler


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
        self.assertEqual(str(e.exception),
                         "Неверный формат данных: должно быть два столбца "
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
        self.assertEqual(str(e.exception),
                         f"Не удалось открыть файл {os.path.abspath(file_name)}"
                         "Проверьте, что он не пуст и в формате csv")
        file_name = root_path + "/test_files/empty.csv"
        with self.assertRaises(handlers.file_handler.FileException) as e:
            handlers.file_handler.FileHandler.read_csv(file_name)
        self.assertEqual(str(e.exception),
                         f"Не удалось открыть файл {os.path.abspath(file_name)}"
                         "Проверьте, что он не пуст и в формате csv")


unittest.main()
