from handlers.handler import Handler
from settings.message import MESSAGES


class HandlerInlineQuery(Handler):
    """
    Класс обработывает входящие текстовые сообщения от нажатия на inline-кнопеи
    """

    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_product(self, call, code):
        """
        Обрабатывает входящие запросы на нажатие inline-кнопок товара
        """
        # создаем запись в БД по факту заказа
        self.DB._add_orders(1, code, 1)
        self.bot.answer_callback_query(call.id,
                                       MESSAGES['product_order'].format(
                                           self.DB.select_single_product_name(code),
                                           self.DB.select_single_product_title(code),
                                           self.DB.select_single_product_price(code),
                                           self.DB.select_single_product_quantity(code)),
                                       show_alert=True)

    def handle(self):
        """
        Обработчик (декоратор) запросов от нажатия на кнопки товаров
        :return:
        """

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = call.data
            if code.isdigit():
                code = int(code)
                self.pressed_btn_product(call, code)
