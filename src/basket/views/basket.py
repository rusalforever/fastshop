from sqladmin import ModelView
from src.basket.models import Basket, BasketItem

class BasketAdmin(ModelView, model=Basket):
    column_list = [Basket.id, Basket.user_id, Basket.created_at, Basket.updated_at]
    column_searchable_list = [Basket.user_id]
    column_filters = [Basket.created_at, Basket.updated_at]

class BasketItemAdmin(ModelView, model=BasketItem):
    column_list = [BasketItem.id, BasketItem.basket_id, BasketItem.product_id, BasketItem.quantity, BasketItem.price]
    column_searchable_list = [BasketItem.product_id]
    column_filters = [BasketItem.basket_id]
