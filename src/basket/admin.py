from sqladmin import ModelView

from src.basket.models.sqlalchemy import Basket

ADMIN_CATEGORY = 'Orders'


class BasketAdmin(ModelView, model=Basket):
    column_list = [Basket.id, Basket.user_id, Basket.price, Basket.status]
    column_searchable_list = [Basket.user_id, Basket.status]
    icon = 'fa-solid fa-shopping-basket'
    category = ADMIN_CATEGORY


def register_basket_admin_views(admin):
    admin.add_view(BasketAdmin)
