from os import path

from models.product import Products
from settings import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_base.dbcore import Base


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
        Инициализация сесии и подключения к БД
        """
        self.engine = create_engine(config.DATABASE)
        session = sessionmaker(bind=self.engine)
        self.session = session()
        if not path.isfile(config.DATABASE):
            Base.metadata.create_all(self.engine)

    def select_all_product(self, category):
        """
        Возвращает все все товары категории
        """
        result = self.session.query(Products).filter_by(category_id=category).all()
        return result

    def close(self):
        """Закрывает сессию"""
        self.session.close()
