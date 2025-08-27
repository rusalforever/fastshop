from datetime import datetime
from enum import Enum
from decimal import Decimal
from typing import (
    List,
    Optional,
)

from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

class BasketStatus(str, Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"

class OrderStatus(str, Enum):
    OPEN = "Open"
    PAID = "Paid"
    SENT = "Sent"
    RECEIVED = "Received"
    CANCELLED = "Cancelled"
    RETURNED = "Returned"

class Product(SQLModel, table=True):
    __tablename__ = 'products'

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    is_active: bool

    categories: List["ProductCategory"] = Relationship(back_populates="product")
    images: List["ProductImage"] = Relationship(back_populates="product")
    stock_records: List["StockRecord"] = Relationship(back_populates="product")
    discounts: List["ProductDiscount"] = Relationship(back_populates="product")
    basket_lines: List["BasketLine"] = Relationship(back_populates="product")
    order_lines: List["OrderLine"] = Relationship(back_populates="product")

class ProductCategory(SQLModel, table=True):
    __tablename__ = 'product_categories'

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    category_id: int = Field(foreign_key="categories.id")

    product: Product = Relationship(back_populates="categories")
    category: "Category" = Relationship(back_populates="products")


class Category(SQLModel, table=True):
    __tablename__ = 'categories'

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: bool
    parent_id: Optional[int] = Field(default=None, foreign_key="categories.id")

    products: List["ProductCategory"] = Relationship(back_populates="category")
    parent: Optional["Category"] = Relationship(
        back_populates="subcategories",
        sa_relationship_kwargs={"remote_side": "Category.id"},
    )
    subcategories: List["Category"] = Relationship(back_populates="parent")


class ProductImage(SQLModel, table=True):
    __tablename__ = 'product_images'

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    original: str
    thumbnail: Optional[str] = None
    caption: Optional[str] = None

    product: Product = Relationship(back_populates="images")


class StockRecord(SQLModel, table=True):
    __tablename__ = 'stock_records'

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    price: float
    quantity: int
    date_created: datetime
    additional_info: Optional[str] = None

    product: Product = Relationship(back_populates="stock_records")


class ProductDiscount(SQLModel, table=True):
    __tablename__ = 'product_discounts'

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    discount_percent: Optional[int] = None
    discount_amount: Optional[float] = None
    valid_from: datetime
    valid_to: datetime

    product: Product = Relationship(back_populates="discounts")

class Basket(SQLModel, table=True):
    __tablename__ = "basket"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    price: Decimal
    status: BasketStatus = Field(
        sa_column_kwargs={"nullable": False, "server_default": "Open"}
    )

    lines: List["BasketLine"] = Relationship(back_populates="basket")
    order: Optional["Order"] = Relationship(back_populates="basket")

class BasketLine(SQLModel, table=True):
    __tablename__ = 'basket_lines'

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    basket_id: int = Field(foreign_key="basket.id")
    quantity: int
    price: Decimal

    product: Product = Relationship(back_populates="basket_lines")
    basket: Basket = Relationship(back_populates="lines")

class Order(SQLModel, table=True):
    __tablename__ = 'orders'

    id: Optional[int] = Field(default=None, primary_key=True)
    number: int = Field(
        sa_column_kwargs={
            "nullable": False,
            "unique": True,
            "server_default": "10000"
        }
    )
    basket_id: int = Field(foreign_key="basket.id")
    user_id: int = Field(foreign_key="users.id")
    address_id: int = Field(foreign_key="addresses.id")
    total_price: Decimal
    shipping_price: Decimal
    shipping_method: Optional[str] = None
    status: OrderStatus = Field(
        sa_column_kwargs={"nullable": False, "server_default": "Open"}
    )
    additional_info: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    basket: Basket = Relationship(back_populates="order")
    lines: List["OrderLine"] = Relationship(back_populates="order")

class OrderLine(SQLModel, table=True):
    __tablename__ = 'order_lines'

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    order_id: int = Field(foreign_key="orders.id")
    quantity: int
    price: Decimal

    product: Product = Relationship(back_populates="order_lines")
    order: Order = Relationship(back_populates="lines")