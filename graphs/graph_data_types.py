class Types:
    def is_pie(self):
        return False

    def is_plot(self):
        return False

    def is_bar(self):
        return False

    def is_hist(self):
        return False


class PieType(Types):
    def is_pie(self):
        return True


class PlotType(Types):
    def is_plot(self):
        return True


class BarType(Types):
    def is_bar(self):
        return True


class HistType(Types):
    def is_hist(self):
        return True
