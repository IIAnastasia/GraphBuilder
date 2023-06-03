import sys

from PyQt5 import QtWidgets

from gui.main_window import UiMainWindow


# запуск приложения
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UiMainWindow()
        self.ui.setupUi(self)


class Application:
    def __init__(self):
        app = QtWidgets.QApplication([])
        application = MainWindow()
        application.show()
        sys.exit(app.exec())


Application()
