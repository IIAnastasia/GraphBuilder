from PyQt5 import QtCore, QtWidgets

from graphs.graph import FileGraph, Base, GraphException
from handlers.file_handler import FileHandler


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.deleteInputButton = QtWidgets.QToolButton(Form)
        self.deleteInputButton.setObjectName("deleteInputButton")
        self.horizontalLayout.addWidget(self.deleteInputButton)
        self.file_name_change = QtWidgets.QPushButton(Form)
        self.file_name_change.setObjectName("file_name_change")
        self.file_name_change.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Fixed))
        self.horizontalLayout.addWidget(self.file_name_change)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.deleteInputButton.setText(_translate("Form", "-"))
        self.file_name_change.setText(_translate("Form", "выберите файл"))

    def setGraphHandler(self, graph_handler):
        self.graph_handler = graph_handler


class Ui_PlotForm:
    def setupUi(self, Form, parentUi):
        self.changeModeToTextButton = QtWidgets.QToolButton(Form)
        self.changeModeToTextButton.setObjectName("changeModeToTextButton")
        parentUi.horizontalLayout.addWidget(self.changeModeToTextButton)
        self.changeModeToTextButton.setText("T")


# Виджет файлового ввода
class FileInputWidget(QtWidgets.QWidget):
    def __init__(self, Form, index, graph_handler, delete_listener, graph_class=Base):
        super(FileInputWidget, self).__init__(Form)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.file_name_change.clicked.connect(self.chooseFile)
        self.ui.deleteInputButton.clicked.connect(self.deleteEquation)
        self.graph_handler = graph_handler
        self.index = index
        self.Form = Form
        self.delete_listener = delete_listener
        self.graph_class = graph_class

    def chooseFile(self):
        file_name, file_type = QtWidgets.QFileDialog.getOpenFileName()
        if file_name != "":
            try:
                data = FileHandler.read_csv(file_name)
                self.ui.file_name_change.setText(file_name)
                self.graph_handler.add_graph(self.graph_class(data), self.index)
            except GraphException as e:
                QtWidgets.QMessageBox.critical(self, "File error",
                                               str(e),
                                               buttons=QtWidgets.QMessageBox.Ok)
            except Exception:
                QtWidgets.QMessageBox.critical(self,
                                               "File error",
                                               "Пустой файл или не в "
                                               "csv-формате. Должен быть csv",
                                               buttons=QtWidgets.QMessageBox.Ok)

    def deleteEquation(self):
        self.graph_handler.remove_graph(self.index)
        self.Form.deleteLater()
        self.delete_listener(self.index)

    def setGraphClass(self, graph_class):
        self.graph_class = graph_class


# Файловый виджет для графика функций. Отличается кнопкой смены типа
class FileInputWidgetPlot(FileInputWidget):
    def __init__(self, Form, changeModeToTextFunction, index, graph_handler,
                 delete_listener):
        super(FileInputWidgetPlot, self).__init__(Form, index, graph_handler,
                                                  delete_listener)
        super(FileInputWidgetPlot, self).setGraphClass(FileGraph)
        self.newUi = Ui_PlotForm()
        self.newUi.setupUi(self, self.ui)
        self.newUi.changeModeToTextButton.clicked.connect(
            lambda: changeModeToTextFunction(index))
