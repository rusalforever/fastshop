from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    Sequence,
    String,
)
from sqlalchemy.orm import relationship

from src.general.databases.postgres import Base


BasketStatusEnum = Enum('Open', 'Closed', 'Cancelled', name='basket_status')
OrderStatusEnum = Enum('Open', 'Paid', 'Sent', 'Received', 'Cancelled', 'Returned', name='order_status')


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003
    name = Column(String, nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    def __str__(self):
        return f"Product(id={self.id}, name={self.name})"


class Basket(Base):
    __tablename__ = 'baskets'

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    price = Column(Numeric(10, 2), nullable=False, default=0)
    status = Column(BasketStatusEnum, nullable=False, default='Open', index=True)

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    user = relationship('User')
    lines = relationship('BasketLine', back_populates='basket', cascade='all, delete-orphan')
    orders = relationship('Order', back_populates='basket')

    def __str__(self):
        return f"Basket(id={self.id}, user_id={self.user_id}, status={self.status})"


class BasketLine(Base):
    __tablename__ = 'basket_lines'

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    basket_id = Column(Integer, ForeignKey('baskets.id'), nullable=False, index=True)

    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(10, 2), nullable=False)

    basket = relationship('Basket', back_populates='lines')
    product = relationship('Product')

    def __str__(self):
        return f"BasketLine(id={self.id}, basket_id={self.basket_id}, product_id={self.product_id}, qty={self.quantity})"


order_number_seq = Sequence('order_number_seq', start=10000)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003
    number = Column(Integer, server_default=order_number_seq.next_value(), unique=True, index=True)

    basket_id = Column(Integer, ForeignKey('baskets.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    address_id = Column(Integer, ForeignKey('user_addresses.id'), nullable=False, index=True)

    total_price = Column(Numeric(10, 2), nullable=False)
    shipping_price = Column(Numeric(10, 2), nullable=False)
    shipping_method = Column(String, nullable=True)
    status = Column(OrderStatusEnum, nullable=False, default='Open', index=True)
    additional_info = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    user = relationship('User')
    basket = relationship('Basket', back_populates='orders')
    address = relationship('UserAddress')
    lines = relationship('OrderLine', back_populates='order', cascade='all, delete-orphan')

    def __str__(self):
        return f"Order(id={self.id}, number={self.number}, status={self.status})"


class OrderLine(Base):
    __tablename__ = 'order_lines'

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False, index=True)

    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(10, 2), nullable=False)

    order = relationship('Order', back_populates='lines')
    product = relationship('Product')

    def __str__(self):
        return f"OrderLine(id={self.id}, order_id={self.order_id}, product_id={self.product_id}, qty={self.quantity})"