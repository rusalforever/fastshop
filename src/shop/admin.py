from sqladmin import ModelView

from src.shop.models.sqlalchemy import (
    Product,
    Basket,
    BasketLine,
    Order,
    OrderLine,
)


ADMIN_CATEGORY = 'Shop'


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name, Product.price, Product.created_at]
    column_searchable_list = [Product.name]
    column_sortable_list = [Product.id, Product.price, Product.created_at]
    icon = 'fa-solid fa-tag'
    category = ADMIN_CATEGORY


class BasketAdmin(ModelView, model=Basket):
    column_list = [Basket.id, Basket.user, Basket.price, Basket.status, Basket.created_at]
    column_searchable_list = [Basket.id, Basket.user]
    column_sortable_list = [Basket.id, Basket.created_at, Basket.status, Basket.price]
    icon = 'fa-solid fa-basket-shopping'
    category = ADMIN_CATEGORY


class BasketLineAdmin(ModelView, model=BasketLine):
    column_list = [BasketLine.id, BasketLine.basket, BasketLine.product_id, BasketLine.quantity, BasketLine.price]
    column_searchable_list = [BasketLine.basket]
    column_sortable_list = [BasketLine.id, BasketLine.quantity, BasketLine.price]
    icon = 'fa-solid fa-list'
    category = ADMIN_CATEGORY


class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.number,
        Order.user,
        Order.basket,
        Order.address,
        Order.total_price,
        Order.shipping_price,
        Order.shipping_method,
        Order.status,
        Order.created_at,
    ]
    column_searchable_list = [Order.number, Order.user]
    column_sortable_list = [Order.id, Order.number, Order.created_at, Order.status, Order.total_price]
    icon = 'fa-solid fa-box'
    category = ADMIN_CATEGORY


class OrderLineAdmin(ModelView, model=OrderLine):
    column_list = [OrderLine.id, OrderLine.order, OrderLine.product_id, OrderLine.quantity, OrderLine.price]
    column_searchable_list = [OrderLine.order]
    column_sortable_list = [OrderLine.id, OrderLine.quantity, OrderLine.price]
    icon = 'fa-solid fa-list-check'
    category = ADMIN_CATEGORY


def register_shop_admin_views(admin):
    admin.add_view(ProductAdmin)
    admin.add_view(BasketAdmin)
    admin.add_view(BasketLineAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(OrderLineAdmin)
