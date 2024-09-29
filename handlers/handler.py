import abc

from data_base.dbalchemy import DBManager
from markup.markup import Keyboards


class Handler(metaclass=abc.ABCMeta):
    def __init__(self, bot):
        self.bot = bot
        self.keyboard = Keyboards()
        self.DB = DBManager()

    @abc.abstractmethod
    def handle(self):
        pass
