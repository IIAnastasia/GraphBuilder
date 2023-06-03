import matplotlib
from PyQt5 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure

import commands.command

matplotlib.use('QT5Agg')


# класс отображения
class GraphCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                             QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


class GraphWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = GraphCanvas()


# оболочка со слайдерами, кнопками перемещения
class GraphWrapperWidget(QtWidgets.QWidget):
    def __init__(self, parent, canvas, graph_handler):
        QtWidgets.QWidget.__init__(self, parent)
        self.graph_handler = graph_handler
        self.up_command = commands.command.UpCommand(graph_handler)
        self.down_command = commands.command.DownCommand(graph_handler)
        self.right_command = commands.command.RightCommand(graph_handler)
        self.left_command = commands.command.LeftCommand(graph_handler)

        self.verticalLayoutWidget = QtWidgets.QWidget()
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalPanel = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.verticalLayoutPanel = QtWidgets.QVBoxLayout(self.verticalPanel)
        self.verticalPanel.setLayout(self.verticalLayoutPanel)
        self.upButton = QtWidgets.QToolButton(self.verticalPanel)
        self.upButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.verticalLayoutPanel.addWidget(self.upButton)
        self.verticalSlider = QtWidgets.QSlider(self.verticalPanel)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.verticalSlider.setValue(0)
        self.verticalLayoutPanel.addWidget(self.verticalSlider)
        self.verticalSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.downButton = QtWidgets.QToolButton(self.verticalPanel)
        self.downButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.verticalLayoutPanel.addWidget(self.downButton)
        self.horizontalLayout.addWidget(self.verticalPanel)
        self.horizontalLayout.addWidget(canvas)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalPanel = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.horizontalLayoutPanel = QtWidgets.QHBoxLayout(self.horizontalPanel)
        self.horizontalPanel.setLayout(self.horizontalLayoutPanel)
        self.leftButton = QtWidgets.QToolButton(self.horizontalPanel)
        self.leftButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontalLayoutPanel.addWidget(self.leftButton)
        self.horizontalSlider = QtWidgets.QSlider(self.horizontalPanel)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayoutPanel.addWidget(self.horizontalSlider)
        self.horizontalSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rightButton = QtWidgets.QToolButton(self.horizontalPanel)
        self.rightButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontalLayoutPanel.addWidget(self.rightButton)
        self.verticalSlider.sliderReleased.connect(self.sliderRelease)
        self.verticalSlider.sliderPressed.connect(self.sliderPress)
        self.verticalSlider.valueChanged.connect(
            lambda: self.execute_activity(
                self.sliderChange, self.verticalSlider.disconnect,
                self.verticalSlider.valueChanged.connect))
        self.horizontalSlider.sliderReleased.connect(self.sliderRelease)
        self.horizontalSlider.sliderPressed.connect(self.sliderPress)
        self.horizontalSlider.valueChanged.connect(
            lambda: self.execute_activity(
                self.sliderChange, self.horizontalSlider.disconnect,
                self.horizontalSlider.valueChanged.connect))
        self.upButton.clicked.connect(
            lambda: self.execute_activity(self.move_graph,
                                          self.upButton.disconnect,
                                          self.upButton.clicked.connect,
                                          self.up_command.execute))
        self.downButton.clicked.connect(
            lambda: self.execute_activity(self.move_graph,
                                          self.downButton.disconnect,
                                          self.downButton.clicked.connect,
                                          self.down_command.execute))
        self.rightButton.clicked.connect(
            lambda: self.execute_activity(self.move_graph,
                                          self.rightButton.disconnect,
                                          self.rightButton.clicked.connect,
                                          self.right_command.execute))
        self.leftButton.clicked.connect(
            lambda: self.execute_activity(self.move_graph,
                                          self.leftButton.disconnect,
                                          self.leftButton.clicked.connect,
                                          self.left_command.execute))
        self.rightButton.setText("→")
        self.leftButton.setText("←")
        self.upButton.setText("↑")
        self.downButton.setText("↓")

        self.horizontalSlider.setValue(0)
        self.verticalLayout_2.addWidget(self.horizontalPanel)
        self.setLayout(self.verticalLayout_2)
        self.increase_shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("ctrl+="),
            self)
        self.increase_shortcut.activated.connect(
            lambda: self.execute_activity(
                self.increase_scale, self.increase_shortcut.disconnect,
                self.increase_shortcut.activated.connect))
        decrease_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("ctrl+-"),
                                                self)
        decrease_shortcut.activated.connect(lambda: self.execute_activity(
            self.decrease_scale, decrease_shortcut.disconnect,
            decrease_shortcut.activated.connect))
        right_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("right"),
                                             self)
        right_shortcut.activated.connect(
            lambda: self.execute_activity(self.move_graph,
                                          right_shortcut.disconnect,
                                          right_shortcut.activated.connect,
                                          self.right_command.execute))
        left_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("left"),
                                            self)
        left_shortcut.activated.connect(
            lambda: self.execute_activity(self.move_graph,
                                          left_shortcut.disconnect,
                                          left_shortcut.activated.connect,
                                          self.left_command.execute))
        up_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("up"),
                                          self)
        up_shortcut.activated.connect(
            lambda: self.execute_activity(self.move_graph,
                                          up_shortcut.disconnect,
                                          up_shortcut.activated.connect,
                                          self.up_command.execute)
        )
        down_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("down"),
                                            self)
        down_shortcut.activated.connect(
            lambda: self.execute_activity(self.move_graph,
                                          down_shortcut.disconnect,
                                          down_shortcut.activated.connect,
                                          self.down_command.execute))
        self.setFocus()

    def execute_activity(self, activity, disconnection, connection, *args):
        disconnection()
        QtCore.QTimer.singleShot(500,
                                 lambda: activity(disconnection, connection,
                                                  *args))

    def move_graph(self, disconnection, connection, command_execution):
        command_execution()
        connection(lambda: self.execute_activity(self.move_graph,
                                                 disconnection,
                                                 connection, command_execution))

    def increase_scale(self, disconnection, connection):
        self.forceSliderChange(self.horizontalSlider,
                               min(100, self.horizontalSlider.value() + 10))
        self.forceSliderChange(self.verticalSlider,
                               min(100, self.verticalSlider.value() + 10))
        commands.command.ScaleCommand(
            self.graph_handler, self.horizontalSlider.value(),
            self.verticalSlider.value()).execute()
        connection(lambda: self.execute_activity(
            self.increase_scale, disconnection, connection))

    def decrease_scale(self, disconnection, connection):
        self.forceSliderChange(self.horizontalSlider,
                               max(0, self.horizontalSlider.value() - 10))
        self.forceSliderChange(self.verticalSlider,
                               max(0, self.verticalSlider.value() - 10))
        commands.command.ScaleCommand(
            self.graph_handler, self.horizontalSlider.value(),
            self.verticalSlider.value()).execute()
        connection(lambda: self.execute_activity(
            self.decrease_scale, disconnection, connection))

    def forceSliderChange(self, slider, value):
        slider.valueChanged.disconnect()
        slider.setValue(value)
        slider.valueChanged.connect(
            lambda: self.execute_activity(self.sliderChange,
                                          slider.disconnect,
                                          slider.valueChanged.connect)
        )

    def sliderPress(self):
        self.sender().valueChanged.disconnect()

    def sliderRelease(self):
        self.sender().valueChanged.connect(
            lambda: self.execute_activity(self.sliderChange,
                                          self.sender().disconnect,
                                          self.sender().valueChanged.connect))
        self.sender().valueChanged.emit(self.sender().value())

    def sliderChange(self, disconnection, connection):
        command = commands.command.ScaleCommand(self.graph_handler,
                                                self.horizontalSlider.value(),
                                                self.verticalSlider.value())
        command.execute()
        connection(
            lambda: self.execute_activity(self.sliderChange, disconnection,
                                          connection))

    # при переключении между типами графиков прячем/показываем оболочку
    def hide(self):
        self.horizontalPanel.hide()
        self.verticalPanel.hide()

    def show(self):
        self.horizontalPanel.show()
        self.verticalPanel.show()
