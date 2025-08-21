import sqlalchemy
from sqlalchemy.orm import relationship

from src.general.databases.postgres import Base
import enum

class BasketStatus(enum.Enum):
    OPEN = 'open'
    CLOSED = 'closed'
    CANCELED = 'canceled'

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    DECIMAL as Decimal,
)

class Basket(Base):
    __tablename__ = 'baskets'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(sqlalchemy.Enum(BasketStatus), nullable=False, default=BasketStatus.OPEN)

    lines = relationship("BasketLine", back_populates="basket", cascade="all, delete-orphan")

class BasketLine(Base):
    __tablename__ = "basket_lines"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    basket_id = Column(Integer, ForeignKey("baskets.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Decimal(10, 2), nullable=False)

    basket = relationship("Basket", back_populates="lines")
    product = relationship("Product")

