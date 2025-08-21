from sqladmin import ModelView

from src.order.models.sqlalchemy import (
    Order,
    OrderLine,
)

ADMIN_CATEGORY = 'Orders'

class OrderAdmin(ModelView, model=Order):
    column_list = [Order.user_id, Order.status]
    column_searchable_list = [Order.user_id]
    icon = 'fa-solid fa-cart-arrow-down'
    category = ADMIN_CATEGORY

class OrderLineAdmin(ModelView, model=OrderLine):
    column_list = [OrderLine.order_id, OrderLine.product_id, OrderLine.quantity, OrderLine.price]
    column_searchable_list = [OrderLine.order_id, OrderLine.product_id]
    icon = 'fa-solid fa-cart-arrow-down'

def register_order_admin_views(admin):
    admin.add_view(OrderAdmin)
    admin.add_view(OrderLineAdmin)