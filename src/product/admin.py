from sqladmin import ModelView

from src.product.models.sqlalchemy import (
    Product
)


ADMIN_CATEGORY = 'Products'


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name]
    column_searchable_list = [Product.name]
    icon = 'fa-solid fa-box'
    category = ADMIN_CATEGORY



def register_product_admin_views(admin):
    admin.add_view(ProductAdmin)
