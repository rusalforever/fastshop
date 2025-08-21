from sqlalchemy import Column, Integer, String

from src.general.databases.postgres import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    def __str__(self):
        return self.name