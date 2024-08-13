from flask import Flask
from sqladmin import ModelView, Admin
from src.catalogue.models.sqlalchemy import (
    Category,
    Product,
    ProductCategory,
    ProductDiscount,
    ProductImage,
    StockRecord,
)

app = Flask(__name__)

CATALOGUE_CATEGORY = 'Catalogue'

class BaseAdmin(ModelView):
    icon = 'fa-solid fa-cog'
    category = CATALOGUE_CATEGORY

    def create_form(self, obj=None):
        form = super().create_form(obj)
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        return form

class ProductAdmin(BaseAdmin):
    model = Product
    column_list = [Product.id, Product.title, Product.is_active]
    column_searchable_list = [Product.title, Product.description]
    form_columns = ['title', 'description', 'short_description', 'is_active']
    column_sortable_list = ['title', 'is_active']
    icon = 'fa-solid fa-box'

class ProductCategoryAdmin(BaseAdmin):
    model = ProductCategory
    column_list = [ProductCategory.product, ProductCategory.category]
    column_searchable_list = [ProductCategory.product_id, ProductCategory.category_id]
    form_columns = ['product', 'category']
    icon = 'fa-solid fa-tags'

class CategoryAdmin(BaseAdmin):
    model = Category
    column_list = [Category.title, Category.is_active, Category.parent]
    column_searchable_list = [Category.title]
    form_columns = ['title', 'description', 'image', 'is_active', 'parent']
    icon = 'fa-solid fa-sitemap'

class ProductImageAdmin(BaseAdmin):
    model = ProductImage
    column_list = [ProductImage.product, ProductImage.original, ProductImage.thumbnail]
    column_searchable_list = [ProductImage.caption]
    form_columns = ['product', 'original', 'thumbnail', 'caption']
    icon = 'fa-solid fa-image'

class StockRecordAdmin(BaseAdmin):
    model = StockRecord
    column_list = [StockRecord.product, StockRecord.price, StockRecord.quantity]
    column_searchable_list = [StockRecord.price, StockRecord.quantity]
    form_columns = ['product', 'price', 'quantity', 'date_created', 'additional_info']
    icon = 'fa-solid fa-warehouse'

class ProductDiscountAdmin(BaseAdmin):
    model = ProductDiscount
    column_list = [ProductDiscount.product, ProductDiscount.discount_percent, ProductDiscount.discount_amount]
    column_searchable_list = [ProductDiscount.valid_from, ProductDiscount.valid_to]
    form_columns = ['product', 'discount_percent', 'discount_amount', 'valid_from', 'valid_to']
    icon = 'fa-solid fa-percent'
    

def register_products_admin_views(admin):
    admin.add_view(ProductAdmin)
    admin.add_view(ProductCategoryAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ProductImageAdmin)
    admin.add_view(StockRecordAdmin)
    admin.add_view(ProductDiscountAdmin)


admin = Admin(app, name='My Admin Panel', template_mode='bootstrap4')

register_products_admin_views(admin)

if __name__ == '__main__':
    app.run()
