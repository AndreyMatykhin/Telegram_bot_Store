import uuid

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from data_base.dbcore import Base
from models.category import Category



class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    #id = Column(String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column(String, index=True)
    title = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    is_active = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'))
    #category_id = Column(String(length=36), ForeignKey('category.id'))
    category = relationship(Category,
                            backref=backref('products',
                                            uselist=True,
                                            cascade='delete, all'))

    def __str__(self):
        return f'{self.name} {self.title} {self.price}'
