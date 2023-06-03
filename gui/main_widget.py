from PyQt5 import QtCore, QtWidgets

import graphs.graph
import graphs.graph_data_types
from gui.file_input_widget import FileInputWidgetPlot, FileInputWidget
from gui.graph_widget import GraphWidget, GraphWrapperWidget
from gui.math_input_widget import MathInputWidget
from handlers.graph_handler import GraphHandler


# Класс основной панели. Состоит из виджета для графика,
# оболочки для перемещений графика, виджетов для ввода
class UIMainWidget:
    def __init__(self, graph_handler):
        self.graph_handler = graph_handler
        self.graph_type = graphs.graph_data_types.PlotType()

    def setupUi(self, Form):
        Form.setWidgetResizable(True)
        Form.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(
            QtCore.QRect(0, 0, 617, 535))
        self.scrollAreaWidgetContents_2.setObjectName(
            "scrollAreaWidgetContents_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(
            self.scrollAreaWidgetContents_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.graphWidget = GraphWidget(self.scrollAreaWidgetContents_2)
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        self.graphWrapper = GraphWrapperWidget(self.scrollAreaWidgetContents_2,
                                               self.graphWidget.canvas,
                                               self.graph_handler)
        self.graphWrapper.setSizePolicy(size_policy)
        self.graphWrapper.setMinimumSize(QtCore.QSize(30, 500))
        self.graphWrapper.setAutoFillBackground(True)
        self.graphWrapper.setObjectName("graphWidget")
        self.graphWrapper.setFocusPolicy(QtCore.Qt.NoFocus)
        self.verticalLayout_4.addWidget(self.graphWrapper)
        self.allInputWidget = QtWidgets.QWidget(Form)
        self.addWidgetsLayout = QtWidgets.QVBoxLayout(self.allInputWidget)
        self.allInputWidget.setLayout(self.addWidgetsLayout)

        self.verticalLayout_4.addWidget(self.allInputWidget)
        self.addWidgetsArray = []
        self.addGraphButton = QtWidgets.QPushButton(
            self.scrollAreaWidgetContents_2)
        self.addGraphButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.addGraphButton.setObjectName("addGraphButton")
        self.verticalLayout_4.addWidget(self.addGraphButton)
        spacer_item = QtWidgets.QSpacerItem(20, 40,
                                            QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacer_item)
        self.widget = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                            QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(size_policy)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacer_item1 = QtWidgets.QSpacerItem(40, 20,
                                             QtWidgets.QSizePolicy.Expanding,
                                             QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacer_item1)
        self.verticalLayout_4.addWidget(self.widget)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        Form.setWidget(self.scrollAreaWidgetContents_2)
        self.retranslateUi(Form)
        self.clickListeners()

    def clickListeners(self):
        self.addGraphButton.clicked.connect(self.addAddWidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.addGraphButton.setText(_translate("MainWindow", "+"))

    # Добавление виджета для добавления графика в список виджетов
    def addAddWidget(self):
        self.addWidgetsArray.append(QtWidgets.QStackedWidget(
            self.allInputWidget))
        if self.graph_type.is_plot():
            self.addWidgetsArray[-1].addWidget(
                MathInputWidget(self.addWidgetsArray[-1],
                                self.change_mode_to_file,
                                len(self.addWidgetsArray) - 1,
                                self.graph_handler,
                                self.delete_graph))
            self.addWidgetsArray[-1].addWidget(
                FileInputWidgetPlot(self.addWidgetsArray[-1],
                                    self.change_mode_to_text,
                                    len(self.addWidgetsArray) - 1,
                                    self.graph_handler, self.delete_graph)
            )
        else:
            graph_class = graphs.graph.Base
            if self.graph_type.is_pie():
                graph_class = graphs.graph.Pie
            elif self.graph_type.is_bar():
                graph_class = graphs.graph.Bar
            elif self.graph_type.is_hist():
                graph_class = graphs.graph.Hist
            self.addWidgetsArray[-1].addWidget(FileInputWidget(
                self.addWidgetsArray[-1], len(self.addWidgetsArray) - 1,
                self.graph_handler, self.delete_graph, graph_class))

        self.addWidgetsLayout.addWidget(self.addWidgetsArray[-1])
        self.graph_handler.imaginary_add()

    # Смена типа виджета для добавления
    def change_mode_to_file(self, index):
        self.addWidgetsArray[index].setCurrentIndex(1)

    # Смена типа виджета для добавления
    def change_mode_to_text(self, index):
        self.addWidgetsArray[index].setCurrentIndex(0)

    # Смена типа графика
    def change_graph_type(self, graph_type):
        self.graph_handler.change_type(graph_type)
        self.graph_type = graph_type
        for i in range(len(self.addWidgetsArray)):
            self.addWidgetsArray[i].deleteLater()
        if graph_type.is_plot():
            self.graphWrapper.show()
        else:
            self.graphWrapper.hide()
        self.addWidgetsArray.clear()

    # удаление виджета для ввода графика
    def delete_graph(self, index):
        self.addWidgetsArray.pop(index)
        for i in range(index, len(self.addWidgetsArray)):
            for j in range(self.addWidgetsArray[i].count()):
                self.addWidgetsArray[i].widget(j).index -= 1


class MainWidget(QtWidgets.QScrollArea):
    def __init__(self, Form):
        super(MainWidget, self).__init__(Form)
        self.graph_handler = GraphHandler()
        self.ui = UIMainWidget(self.graph_handler)
        self.ui.setupUi(self)
        self.graph_handler.graph_view_handler.set_figure(
            self.ui.graphWidget.canvas.fig)
        self.graph_handler.graph_view_handler.set_canvas(
            self.ui.graphWidget.canvas)

    def change_graph_type(self, graph_type):
        self.ui.change_graph_type(graph_type)
