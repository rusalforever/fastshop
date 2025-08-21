from sqladmin import ModelView

from src.basket.models.sqlalchemy import (
Basket,
BasketLine,
)

ADMIN_CATEGORY = 'Shopping Cart'

class BasketAdmin(ModelView, model=Basket):
    column_list = [Basket.id, Basket.user_id, Basket.price, Basket.status]
    column_searchable_list = [Basket.user_id]
    icon = 'fa-solid fa-shopping-cart'
    category = ADMIN_CATEGORY

class BasketLineAdmin(ModelView, model=BasketLine):
    column_list = [BasketLine.id, BasketLine.basket_id, BasketLine.product_id, BasketLine.quantity, BasketLine.price]
    column_searchable_list = [BasketLine.basket_id, BasketLine.product_id]
    icon = 'fa-solid fa-shopping-cart-arrow-down'

def register_basket_admin_views(admin):
    admin.add_view(BasketAdmin)
    admin.add_view(BasketLineAdmin)