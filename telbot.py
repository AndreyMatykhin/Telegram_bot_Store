from telebot import TeleBot

from handlers.handler_main import HandlerMain
from settings import config


class TelBot:
    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self):
        self.token = config.TOKEN
        self.bot = TeleBot(self.token)
        self.handler = HandlerMain(self.bot)

    def start(self):
        self.handler.handle()

    def run_bot(self):
        self.start()
        self.bot.infinity_polling()


if __name__ == '__main__':
    bot = TelBot()
    bot.run_bot()
