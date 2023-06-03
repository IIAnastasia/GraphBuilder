from PyQt5 import QtCore, QtWidgets

import graphs.graph_data_types


class UILeftPanel:
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWidgetResizable(True)
        self.listener = None
        self.scrollAreaWidgetContents = QtWidgets.QWidget(Form)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 153, 535))
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.plotButton = QtWidgets.QPushButton(Form)
        self.plotButton.setObjectName("plotButton")
        self.verticalLayout_7.addWidget(self.plotButton)
        self.pieButton = QtWidgets.QPushButton(Form)
        self.pieButton.setObjectName("pieButton")
        self.verticalLayout_7.addWidget(self.pieButton)
        self.barButton = QtWidgets.QPushButton(Form)
        self.barButton.setObjectName("barButton")
        self.verticalLayout_7.addWidget(self.barButton)
        self.histButton = QtWidgets.QPushButton(Form)
        self.histButton.setObjectName("histButton")
        self.verticalLayout_7.addWidget(self.histButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40,
                                           QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem)
        Form.setWidget(self.scrollAreaWidgetContents)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.connectButtons()

    def connectButtons(self):
        self.plotButton.clicked.connect(lambda: self.listener(
            graphs.graph_data_types.PlotType()))
        self.pieButton.clicked.connect(lambda: self.listener(
            graphs.graph_data_types.PieType()))
        self.barButton.clicked.connect(lambda: self.listener(
            graphs.graph_data_types.BarType()))
        self.histButton.clicked.connect(lambda: self.listener(
            graphs.graph_data_types.HistType()))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.plotButton.setText(_translate("Form", "График"))
        self.pieButton.setText(_translate("Form", "Пирог"))
        self.barButton.setText(_translate("Form", "Столбчатая"))
        self.histButton.setText(_translate("Form", "Гистограмма"))


class LeftPanel(QtWidgets.QScrollArea):
    def __init__(self, Form):
        super(LeftPanel, self).__init__(Form)
        self.Form = Form
        self.ui = UILeftPanel()
        self.ui.setupUi(self)

    def set_change_window_listener(self, listener):
        self.ui.listener = listener
