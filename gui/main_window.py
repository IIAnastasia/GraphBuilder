from PyQt5 import QtCore, QtWidgets

from gui.left_panel import LeftPanel
from gui.main_widget import MainWidget


# Основное окно. Состоит из левой панели, занимающей четверть экрана и основной
class UiMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 650)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.leftPanelWidget = LeftPanel(self.centralwidget)
        self.leftPanelWidget.setObjectName("leftPanelWidget")
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                            QtWidgets.QSizePolicy.Preferred)
        self.leftPanelWidget.setSizePolicy(size_policy)
        self.horizontalLayout.addWidget(self.leftPanelWidget)
        self.leftPanelWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.leftPanelWidget.set_change_window_listener(self.changeWindow)

        self.mainWidget = MainWidget(self.centralwidget)
        self.mainWidget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.horizontalLayout.addWidget(self.mainWidget)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def changeWindow(self, graph_type):
        self.mainWidget.change_graph_type(graph_type)
