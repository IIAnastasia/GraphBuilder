Проект построитель графиков

В проекте используется паттерн Bridge для разделения логик:
Работа с файлами - FileHandler
Отображение - MainWindow
Работа с отображением графиков - BaseDataHandler, BaseViewHandler и наследники
Работа с хранением графиков - Base и наследники

Паттерн Command для объединения графических кнопок и горячих клавиш


При запуске программы пользователь выбирает тип графика. Далее он вводит данные. Если пользователь работает с графиком функции, ему доступен текстовый ввод и файловый. В остальных случаях только файловый. При выборе файла вызывается FileHandler. В FileHandler пока единственный метод read_csv. В дальнейшем будут другие. 
Данные считываются, вызывается GraphHandler для отрисовки графика. GraphHandler состоит из 2 частей: BaseDataHandler и BaseViewHandler. BaseDataHandler заботится о подготовке численных данных, BaseViewHandler - об отрисовке. Для графиков функций используются классы-наследники GraphDataHandler и GraphViewHandler соответственно. Для остальных типов графиков сейчас используются классы BaseDataHandler и OtherDataHandler. Если потребуется другая функциональность будет создан другой наследник. Поддержанием типов занимается GraphHandler. Данные графиков функций хранятся в классах FileGraph и TextGraph в зависимости от типа ввода. Оба класса наследуются от класса Graph, который наследуется от класса Base. Для остальных типов графиков используется класс Base. Если потребуется другая функциональность, относледуется другой класс. Класс Base просто хранит данные. Класс Graph добавляет работу с диапазонами. TextGraph и FileGraph специализируют ее. Graph может быть пустым, TextGraph и FileGraph должны отвечать за какой-то график. FileGraph хранит все точки графика. Меняет только свой диапазон. TextGraph вычисляет свои точки при изменении диапазона. TextGraph работет с объектом класса StringParser, который конструируется от математической строки, позволяет по значениям x и y узнать выполняется ли равенство. Для графиков функций доступно масштабирование и перемещение. Перемещение выполняется кнопками вверх/вниз/вправо/влево или соответствующими клавишами. Масштабирование - при помощи ползунков или сочетаний ctrl+= и ctrl+-. Во все случаях вызываются наследники класса Command, которые вызывают необходимые методы в GraphHandler



