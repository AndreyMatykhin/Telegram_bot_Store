from handlers.handler import Handler


class HandlerCommands(Handler):
    """
    Класс обрабатывает входящие комманды /start, /help и п.т.
    """

    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        """
        Обрабатывает входящие /start команды
        :param message:
        :return:
        """
        self.bot.send_message(message.chat.id,
                              f'{message.from_user.first_name}, здравствуйте! Жду дальнейших задач.',
                              reply_markup=self.keyboards.start_menu())
    def handle(self):
        # Обработчик/декоратор сообщений, который обрабатывает входящие /start команды
        @self.bot.message_handler(commands=['start'])
        def handle(message):
            print(message)
            if message.text == '/start':
                self.pressed_btn_start(message)