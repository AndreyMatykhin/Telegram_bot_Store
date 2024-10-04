import uuid

from sqlalchemy import Column, Integer, String, Boolean

from data_base.dbcore import Base


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    # id = Column(String(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    name = Column(String, index=True)
    is_active = Column(Boolean)

    def __str__(self):
        return self.name
