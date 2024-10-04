# импортируем специальные типы телеграм бота для создания элементов интерфейса
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
# импортируем класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager
# импортируем настройки и утилиты
from settings import config


class Keyboards:
    """
    Класс Keyboards предназначен для создания и разметки интерфейса бота
    """

    # инициализация разметки
    def __init__(self):
        self.markup = None
        # инициализируем менеджер для работы с БД
        self.DB = DBManager()

    def set_btn(self, name, step=0, quantity=0):
        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self):
        """
        Срздает разметку кнопок в основном меню и возвращает разметку
        :return:
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('CHOOSE GOODS')
        itm_btn_2 = self.set_btn('INFO')
        itm_btn_3 = self.set_btn('SETTINGS')
        # расположение кнопок в меню
        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2, itm_btn_3)
        return self.markup

    def info_menu(self):
        """
        Создает разметку кнопок в меню 'О магазине'
        :return:
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        self.markup.row(itm_btn_1)
        return self.markup

    def settings_menu(self):
        """
        Сздает разметку кнопок в меню 'Настройки'
        :return:
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('<<')
        self.markup.row(itm_btn_1)
        return self.markup

    @staticmethod
    def remove_menu():
        """
        Удаляет меню
        :return:
        """
        return ReplyKeyboardRemove()

    def category_menu(self):
        """
        Создает разметку кнопок в меню каегорий товарови возвращает эту разметку
        :return:
        """
        self.markup = ReplyKeyboardMarkup(True, True, row_width=1)
        self.markup.add(self.set_btn('SEMIPRODUCT'))
        self.markup.add(self.set_btn('GROCERY'))
        self.markup.add(self.set_btn('ICE_CREAM'))
        self.markup.row(self.set_btn('<<'), self.set_btn('ORDER'))
        return self.markup

    @staticmethod
    def set_inline_btn(name):
        """
        Создает и возвращает инлайн-кнопку по входным параметрам
        """
        return InlineKeyboardButton(str(name),
                                    callback_data=str(name.id))

    def set_select_category(self, category):
        """
        Создает разметку в выбранной категории товара и возвращает разметку
        :param category:
        :return:
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        # загружаем в названия инлайн-кнопок данные из БД в соответствие с категорией товара
        for itm in self.DB.select_all_product(category):
            self.markup.add(self.set_inline_btn(itm))
        return self.markup
