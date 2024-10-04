import uuid

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship, backref

from data_base.dbcore import Base
from models.product import Products



class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    # id = Column(String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    quantity = Column(Integer)
    data = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id'))
    # product_id = Column(String(length=36), ForeignKey('products.id'))
    user_id = Column(String(length=36))
    products = relationship(Products,
                            backref=backref('orders',
                                            uselist=True,
                                            cascade='delete, all'))

    def __str__(self):
        return f'{self.quantity} {self.data}'
