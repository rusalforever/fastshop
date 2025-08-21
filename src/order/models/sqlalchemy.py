from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from src.general.databases.postgres import Base

class OrderStatus(enum.Enum):
    OPEN = "Open"
    PAID = "Paid"
    SENT = "Sent"
    RECEIVED = "Received"
    CANCELLED = "Cancelled"
    RETURNED = "Returned"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, unique=True, index=True, default=10000)
    basket_id = Column(Integer, ForeignKey("baskets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address_id = Column(Integer, ForeignKey("user_addresses.id"), nullable=False)

    total_price = Column(Numeric(10, 2))
    shipping_price = Column(Numeric(10, 2))
    shipping_method = Column(String, nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.OPEN)
    additional_info = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(datetime.now().astimezone().tzinfo))

    lines = relationship("OrderLine", back_populates="order")

class OrderLine(Base):
    __tablename__ = "order_lines"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="lines")
    product = relationship("Product")