import abc

from data_base.dbalchemy import DBManager
from markup.markup import Keyboards


class Handler(metaclass=abc.ABCMeta):
    def __init__(self, bot):
        # получаем объект бота
        self.bot = bot
        # инициализируем разметку кнопок
        self.keyboards = Keyboards()
        # инициализируем менеджер для работы с БД
        self.DB = DBManager()

    @abc.abstractmethod
    def handle(self):
        pass
