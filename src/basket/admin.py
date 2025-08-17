from enum import Enum
from sqladmin import ModelView
from typing import List
from sqlmodel import Field
from src.basket.models.database import Basket, BasketLine
from src.users.models.database import User

ADMIN_CATEGORY = 'Shop'

class BasketStatus(str, Enum):
    OPEN = 'Open'
    CLOSED = 'Closed'
    CANCELLED = 'Cancelled'

class BasketAdmin(ModelView, model=Basket):
    column_list = [Basket.id, Basket.user_id, Basket.status, Basket.created_at, Basket.updated_at]
    column_searchable_list = [Basket.user_id]
    column_filters = [Basket.status]
    icon = 'fa-solid fa-shopping-basket'
    category = ADMIN_CATEGORY

class BasketLineAdmin(ModelView, model=BasketLine):
    column_list = [BasketLine.id, BasketLine.basket_id, BasketLine.product_id, BasketLine.quantity, BasketLine.price]
    column_searchable_list = [BasketLine.product_id]
    icon = 'fa-solid fa-box'
    category = ADMIN_CATEGORY

def register_basket_admin_views(admin):
    admin.add_view(BasketAdmin)
    admin.add_view(BasketLineAdmin)
