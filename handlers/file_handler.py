import pandas
import os

class FileException(Exception):
    pass


class FileHandler:
    @staticmethod
    def read_csv(filename, delimiter=","):
        try:
            csv_file = pandas.read_csv(filename, delimiter=delimiter,
                                       header=None)
        except Exception:
            raise FileException(f"Не удалось открыть файл {os.path.abspath(filename)}"
                                "Проверьте, что он не пуст и в формате csv")
        return csv_file
