from src.users.admin import register_hr_admin_views
from src.shop.admin import register_shop_admin_views


def register_admin_views(admin):
    register_hr_admin_views(admin=admin)
    register_shop_admin_views(admin=admin)
