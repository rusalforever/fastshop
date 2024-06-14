from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Numeric,
    Enum
)

import enum

from src.general.databases.postgres import Base


class BasketStatus(enum.Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"


class Basket(Base):
    __tablename__ = 'baskets'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(BasketStatus), default=BasketStatus.OPEN, nullable=False)
