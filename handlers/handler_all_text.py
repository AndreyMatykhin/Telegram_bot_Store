# Импортируем класс-родитель
from xml.sax import parse

from handlers.handler import Handler
from settings import config
# Импортируем ответ пользователю
from settings.message import MESSAGES


class HandlerAllText(Handler):
    """
    Класс, обрабатывающий текстовые сообщения от нажатия кнопки
    """

    def __init__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_btn_info(self, message):
        """
        Отображает входящие текстовое сообщение от нажатия на кнопку 'О магазине'
        :param message:
        :return:
        """
        self.bot.send_message(message.chat.id,
                              MESSAGES['trading store'],
                              parse_mode="HTML",
                              reply_markup=self.keyboards.info_menu())

    def pressed_btn_settings(self, message):
        """
        Отображает входяащие текстовое сообщение от нажатия на кнопку 'Настройки'
        :param message:
        :return:
        """
        self.bot.send_message(message.chat.id,
                              MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keyboards.settings_menu())

    def pressed_btn_back(self, message):
        """
        Отображает входящие текстовое сообщение от нажатия на кнопку 'Назад'
        :param message:
        :return:
        """
        self.bot.send_message(message.chat.id,
                              "вы вернулись назад",
                              reply_markup=self.keyboards.start_menu())

    def pressed_btn_category(self, message):
        """
        Обработка события нажатия кнопки 'Выбрать товар'. А точнее выбор категории товаров
        :param message:
        :return:
        """
        self.bot.send_message(message.chat.id,
                              "Каталог категории товаров",
                              reply_markup=self.keyboards.remove_menu())
        self.bot.send_message(message.chat.id,
                              "Сделай свой выбор",
                              reply_markup=self.keyboards.category_menu())

    def present_btn_product(self, message, product):
        """
        Обработка событи янажатия на кнопку 'Выбрать товар'. А точнее это выбор товара из категории
        :param message:
        :param product:
        :return:
        """
        self.bot.send_message(message.chat.id,
                              'Категория' + config.KEYBOARD[product],
                              reply_markup=self.keyboards.set_select_category(config.CATEGORY[product]))
        self.bot.send_message(message.chat.id,
                              'Ok',
                              reply_markup=self.keyboards.category_menu())

    def handle(self):
        # Обработчик/декоратор, который обрабатываетвходящие текстовые сообщения от нажатия кнопок
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            # *************Меню**************
            if message.text == config.KEYBOARD['CHOOSE GOODS']:
                self.pressed_btn_category(message)
            if message.text == config.KEYBOARD['INFO']:
                self.pressed_btn_info(message)
            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)
            if message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)
            if message.text == config.KEYBOARD['ORDER']:
                # если есть заказы
                if self.DB.count_row_order() > 0:
                    self.present_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id,
                                          MESSAGES['no_orders'],
                                          parse_mode='HTML',
                                          reply_markup=self.keyboards.category_menu())
            # ********** меню (категории товара, ПФ, Бакалея, Мороженое)**********
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.present_btn_product(message, 'SEMIPRODUCT')
            if message.text == config.KEYBOARD['GROCERY']:
                self.present_btn_product(message, 'GROCERY')
            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.present_btn_product(message, 'ICE_CREAM')

    def present_btn_order(self, message):
        """ Обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Заказ'. """
        # обнуляем данные шага
        self.step = 0
        # получаем список всех товаров в заказе
        count = self.DB.select_all_product_id()
        # получаем количество по каждой позиции товара в заказе
        quantity = self.DB.select_order_quantity(count[self.step])
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        """ Отправляет ответ пользователю при выполнении различных действий """
        self.bot.send_message(message.chat.id,
                              MESSAGES['order_number'].format(self.step + 1),
                              parse_mode='HTML')
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].format(self.DB.select_single_product_name(product_id),
                                                       self.DB.select_single_product_title(product_id),
                                                       self.DB.select_single_product_price(product_id),
                                                       self.DB.select_order_quantity(product_id)),
                              parse_mode='HTML',
                              reply_markup=self.keyboards.order_menu(self.step, quantity))
