class Command:
    def __init__(self, graph_handler):
        self.graph_handler = graph_handler


class RightCommand(Command):
    def execute(self):
        self.graph_handler.move(10, 0)


class LeftCommand(Command):
    def execute(self):
        self.graph_handler.move(-10, 0)


class UpCommand(Command):
    def execute(self):
        self.graph_handler.move(0, 10)


class DownCommand(Command):
    def execute(self):
        self.graph_handler.move(0, -10)


class ScaleCommand(Command):
    def __init__(self, graph_handler, x_percent=0, y_percent=0):
        super(ScaleCommand, self).__init__(graph_handler)
        self.x_percent = x_percent
        self.y_percent = y_percent

    def execute(self):
        self.graph_handler.change_scale(self.x_percent, self.y_percent)
