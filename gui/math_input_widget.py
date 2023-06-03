from PyQt5 import QtCore, QtWidgets

from graphs.graph import TextGraph


class UiForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.deleteInputButton = QtWidgets.QToolButton(Form)
        self.deleteInputButton.setObjectName("deleteInputButton")
        self.horizontalLayout.addWidget(self.deleteInputButton)
        self.mathInputLine = QtWidgets.QLineEdit(Form)
        self.mathInputLine.setObjectName("mathInputLine")
        self.horizontalLayout.addWidget(self.mathInputLine)
        self.addInputButton = QtWidgets.QPushButton(Form)
        self.addInputButton.setObjectName("addInputButton")
        self.horizontalLayout.addWidget(self.addInputButton)
        self.changeModeToFileButton = QtWidgets.QToolButton(Form)
        self.changeModeToFileButton.setObjectName("changeModeToFileButton")
        self.horizontalLayout.addWidget(self.changeModeToFileButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.deleteInputButton.setText(_translate("Form", "-"))
        self.addInputButton.setText(_translate("Form", "+"))
        self.changeModeToFileButton.setText(_translate("Form", "F"))


class MathInputWidget(QtWidgets.QWidget):
    def __init__(self, Form, change_mode_to_file_function, index, graph_handler,
                 delete_listener):
        super(MathInputWidget, self).__init__(Form)
        self.ui = UiForm()
        self.ui.setupUi(self)
        self.ui.changeModeToFileButton.clicked.connect(
            lambda: change_mode_to_file_function(index))
        self.graph_handler = graph_handler
        self.ui.addInputButton.clicked.connect(
            lambda: self.execute_activity(
                self.addEquation, self.ui.addInputButton.disconnect,
                self.ui.addInputButton.clicked.connect))
        self.ui.deleteInputButton.clicked.connect(self.deleteEquation)
        self.index = index
        self.Form = Form
        self.delete_listener = delete_listener

    def execute_activity(self, activity, disconnection, connection, *args):
        disconnection()
        QtCore.QTimer.singleShot(500,
                                 lambda: activity(disconnection, connection,
                                                  *args))

    def addEquation(self, disconnection, connection):
        try:
            self.graph_handler.add_graph(
                TextGraph(self.ui.mathInputLine.text()), self.index)
            connection(lambda: self.execute_activity(
                self.addEquation, disconnection, connection))
        except Exception:
            QtWidgets.QMessageBox.critical(self, "Input error",
                                           "Неверный формат. Должно быть:\n"
                                           "Переменные: x, y\n"
                                           "Операторы: +, -, *, /, ^\n"
                                           "Функции: sin(x), cos(x), tan(x), "
                                           "arcsin(x), arccos(x), arctan(x), "
                                           "abs(x), log(x), log10(x), exp(x)",
                                           buttons=QtWidgets.QMessageBox.Ok)

    def deleteEquation(self):
        self.graph_handler.remove_graph(self.index)
        self.Form.deleteLater()
        self.delete_listener(self.index)
