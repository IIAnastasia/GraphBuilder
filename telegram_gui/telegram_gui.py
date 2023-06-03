import time

import pandas
import telebot
from io import BytesIO
import handlers.graph_handler
import graphs.graph
import graphs.graph_data_types
import matplotlib.pyplot as plt


bot = telebot.TeleBot('your_token')
session_storage = {}


def exception_decorator(func):
    def wrapper(message):
        try:
            return func(message)
        except graphs.graph.GraphException as e:
            bot.reply_to(message, str(e))
    return wrapper


class UserInfo:
    def __init__(self, graph_type=graphs.graph_data_types.PlotType()):
        self.graph_type = graph_type
        self.graph_handler = handlers.graph_handler.GraphHandler(False)
        self.graph_handler.graph_view_handler.figure = plt.figure()
        self.last_graph_id = 1
        self.graphs_indexes = {}

    def change_type(self, new_type):
        self.graph_type = new_type
        self.graph_handler.change_type(self.graph_type)
        self.last_graph_id = 1
        self.graphs_indexes.clear()


@bot.message_handler(commands=['start'])
def start_message(message):
    session_storage[message.chat.id] = UserInfo()
    bot.send_message(message.chat.id,
                     'Graph Builder - бот для построения графиков.\n'
                     'Доступны 4 вида графиков: /plot, /pie, /bar, /hist.\n'
                     'Для всех 4 графиков доступен ввод данных в формате csv. '
                     'Столбцы должны быть без заголовков. \n'
                     'Для графика функции (/plot) также доступен текстовый ввод графика. \n'
                     'Формат ввода: "/func x + y = 5"\n'
                     'После ввода графика вы получаете идентификатор графика\n'
                     'Если захотите удалить определенный график, введите "/delete id", где id - полученный идентификатор\n'
                     'Чтобы вывести построенные графики введите /download')


@bot.message_handler(content_types=['document'])
@exception_decorator
def handle_docs(message):
    chat_id = message.chat.id
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    data = pandas.read_csv(BytesIO(downloaded_file), header=None)
    if chat_id not in session_storage:
        session_storage[chat_id] = UserInfo()
    user_info = session_storage[chat_id]
    if user_info.graph_type.is_plot():
        add_graph(graphs.graph.FileGraph(data), user_info, message)
    elif user_info.graph_type.is_pie():
        add_graph(graphs.graph.Pie(data), user_info, message)
    elif user_info.graph_type.is_bar():
        add_graph(graphs.graph.Bar(data), user_info, message)
    elif user_info.graph_type.is_hist():
        add_graph(graphs.graph.Hist(data), user_info, message)


@bot.message_handler(commands=["func"])
@exception_decorator
def handle_math_input(message):
    chat_id = message.chat.id
    if chat_id not in session_storage:
        session_storage[chat_id] = UserInfo()
    if not session_storage[chat_id].graph_type.is_plot():
        bot.reply_to(message, "Ввод формул доступен только для графиков функций. "
                              "Введите /plot для перехода в режим графиков функций")
    else:
        user_info = session_storage[chat_id]
        text_graph = graphs.graph.TextGraph(" ".join(message.text.split()[1:]))
        add_graph(text_graph, user_info, message)


def add_graph(graph, user_info, message):
    index = user_info.graph_handler.imaginary_add()
    user_info.graph_handler.add_graph(graph, index)
    user_info.graphs_indexes[user_info.last_graph_id] = index
    user_info.last_graph_id += 1
    bot.reply_to(message,
                 f"Добавлен график с id {user_info.last_graph_id - 1}")


@bot.message_handler(commands=["delete"])
def handle_delete(message):
    try:
        chat_id = message.chat.id

        check_in_storage(chat_id)
        delta = 0
        user_info = session_storage[chat_id]
        delete_ids = [int(i) for i in message.text.split()[1:]]
        current_id_index = 0
        if any(i not in user_info.graphs_indexes.keys() for i in delete_ids):
            raise IndexError("Неверный id")
        for i in sorted(user_info.graphs_indexes.keys()):
            if current_id_index < len(delete_ids) and i == delete_ids[current_id_index]:
                user_info.graph_handler.remove_graph(user_info.graphs_indexes[i] - delta)
                del user_info.graphs_indexes[i]
                delta += 1
                current_id_index += 1
            else:
                user_info.graphs_indexes[i] -= delta
    except IndexError as e:
        bot.reply_to(message, str(e))



@bot.message_handler(commands=["plot"])
def handle_plot_type(message):
    chat_id = message.chat.id
    check_in_storage(chat_id)
    session_storage[chat_id].change_type(graphs.graph_data_types.PlotType())


@bot.message_handler(commands=["pie"])
def handle_pie_type(message):
    chat_id = message.chat.id
    check_in_storage(chat_id)
    session_storage[chat_id].change_type(graphs.graph_data_types.PieType())


@bot.message_handler(commands=["bar"])
def handle_bar_type(message):
    chat_id = message.chat.id
    check_in_storage(chat_id)
    session_storage[chat_id].change_type(graphs.graph_data_types.BarType())


@bot.message_handler(commands=["hist"])
def handle_hist_type(message):
    chat_id = message.chat.id
    check_in_storage(chat_id)
    session_storage[chat_id].change_type(graphs.graph_data_types.HistType())


@bot.message_handler(commands=["download"])
def handle_download(message):
    chat_id = message.chat.id
    plot_file = BytesIO()
    plot_file.name = "image.png"
    check_in_storage(chat_id)
    user_info = session_storage[chat_id]
    user_info.graph_handler.download(plot_file)
    plot_file.seek(0)
    bot.send_photo(chat_id, plot_file)

@bot.message_handler(commands=["stop"])
def handle_stop(message):
    check_in_storage(message.chat.id)
    del session_storage[message.chat.id]


def check_in_storage(chat_id):
    if chat_id not in session_storage:
        session_storage[chat_id] = UserInfo()


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)