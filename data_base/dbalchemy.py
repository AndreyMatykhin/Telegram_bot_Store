from datetime import datetime
from os import path

from models.order import Order
from models.product import Products
from settings import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_base.dbcore import Base


def _convert(list_convert):
    return [itm[0] for itm in list_convert]


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    """
    Класс-менеджер для работы с БД
    """

    def __init__(self):
        """
        Инициализация сессии и подключения к БД
        """
        self.engine = create_engine(config.DATABASE)
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)

    def select_all_product(self, category):
        """
        Возвращает все все товары категории
        """
        result = self._session.query(Products).filter_by(category_id=category).all()
        return result

    def close(self):
        """Закрывает сессию"""
        self._session.close()

    def _add_orders(self, quantity, product_id, user_id):
        """
        Метод заполнения заказа
        :param quantity:
        :param product_id:
        :param user_id:
        :return:
        """
        # получение списка всех продуктов
        all_id_product = self.select_all_product_id()
        # если данные есть в списке, обновляем  таблицы заказаи продуктов
        if product_id in all_id_product:
            quantity_order = self.select_order_quantity(product_id)
            quantity_order += 1
            self.update_order_value(product_id, 'quantity', quantity_order)
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
            return
        # если данных нет, создаем новый лбъет заказа
        else:
            order = Order(quantity=quantity, product_id=product_id, user_id=user_id, data=datetime.now())
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
        self._session.add(order)
        self._session.commit()
        self.close()

    def select_all_product_id(self):
        """
        Возвращает все id товара в заказе
        :return:
        """
        result = self._session.query(Order.product_id).all()
        return _convert(result)

    def select_order_quantity(self, product_id):
        """Возвращает количество товара в заказе"""
        result = self._session.query(Order.quantity).filter_by(product_id=product_id).one()
        self.close()
        return result.quantity

    def update_order_value(self, product_id, name, value):
        """ Обновляет данные указанные в позиции заказа в соответствии с номером товара"""
        self._session.query(Order).filter_by(product_id=product_id).update({name: value})
        self._session.commit()
        self.close()

    def select_single_product_quantity(self, rownum):
        """
        Возвращает количество товара на складе в соответствии с номером товара - rownum.
        Этот номер определяется при выборе товара в интерфейсе.
        """
        result = self._session.query(Products.quantity).filter_by(id=rownum).one()
        self.close()
        return result.quantity

    def update_product_value(self, rownum, name, value):
        """ Обновляет количество товара на складе в соответствии с номером товара - rownum """
        self._session.query(Products).filter_by(id=rownum).update({name: value})
        self._session.commit()
        self.close()

    def select_single_product_name(self, rownum):
        """ Возвращает название товара в соответствии с номером товара - rownum """
        result = self._session.query(Products.name).filter_by(id=rownum).one()
        self.close()
        return result.name

    def select_single_product_title(self, rownum):
        """ Возвращает торговую марку товара в соответствии с номером товара - rownum """
        result = self._session.query(Products.title).filter_by(id=rownum).one()
        self.close()
        return result.title

    def select_single_product_price(self, rownum):
        """ Возвращает цену товара в соответствии с номером товара - rownum """
        result = self._session.query(Products.price).filter_by(id=rownum).one()
        self.close()
        return result.price

    def count_row_order(self):
        """ Возвращает количество позиций в заказе """
        result = self._session.query(Order).count()
        self.close()
        return result

    def delete_order(self, product_id):
        """ Удаляет данные указанной строки заказа """
        self._session.query(Order).filter_by(product_id=product_id).delete()
        self._session.commit()
        self.close()

    def get_total_coast(self):
        """ Возвращает общую стоимость товара """
        # получаем список все product_id заказа
        all_product_id = self.select_all_product_id()
        # получаем список стоимость по всем позициям заказа в виде обычного списка
        all_price = [self.select_single_product_price(itm) for itm in all_product_id]
        # получаем список количества по всем позициям заказа в виде обычного списка
        all_quantity = [self.select_order_quantity(itm) for itm in all_product_id]
        # Считает общую сумму заказа и возвращает результат

        # order_total_coast = 0
        # for i, one_price in  enumerate(all_price):
        #    order_total_coast+=all_quantity[i]*one_price

        order_total_coast = sum([x * y for x, y in zip(all_price, all_quantity)])
        return order_total_coast

    def get_total_quantity(self):
        """ Возвращает общее количество заказанной единицы товара """
        # получаем список все product_id заказа
        all_product_id = self.select_all_product_id()
        # получаем список количества по всем позициям заказа в виде обычного списка
        all_quantity = [self.select_order_quantity(itm) for itm in all_product_id]
        return sum(all_quantity)

    def delete_all_order(self):
        """ Удаляет данные всего заказа """
        all_id_order = self.select_all_order_id()
        for itm in all_id_order:
            self._session.query(Order).filter_by(id=itm).delete()
            self._session.commit()
        self.close()

    def select_all_order_id(self):
        """ Возвращает все id заказа """
        result = self._session.query(Order.id).all()
        self.close()
        return _convert(result)
