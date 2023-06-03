import numexpr


class StringParser:
    def __init__(self, string, variables):
        # Подготовка строки для numexpr
        self.operator = "="
        self.string = string.replace("^", "**")
        if "=" in string:
            parts = self.string.split(self.operator)
            self.string = f"{parts[0]}-({parts[1]})"
        self.vars = variables
        self.reload()

    def check(self, variables, calc_error):
        # check для одной и той же строки вызывается много раз подряд
        # чтобы не numexpr не парсил каждый раз check check пересчитывает
        # значения для сохраненной в numexpr строки
        if self.operator == "=":
            return -calc_error < numexpr.re_evaluate(variables) <= calc_error

    # при смене строки метод numexpr парсит заново
    def reload(self):
        numexpr.evaluate(self.string, self.vars)
