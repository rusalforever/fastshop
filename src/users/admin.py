from sqladmin import ModelView
from src.users.models.sqlalchemy import User, UserAddress, Basket

ADMIN_CATEGORY = 'Accounts'


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.phone_number]
    column_searchable_list = [User.email, User.first_name, User.last_name]
    icon = 'fa-solid fa-user'
    category = ADMIN_CATEGORY


class UserAddressAdmin(ModelView, model=UserAddress):
    column_list = [UserAddress.user, UserAddress.title, UserAddress.street]
    column_searchable_list = [UserAddress.user, UserAddress.title, UserAddress.city, UserAddress.street]
    icon = 'fa-solid fa-address-book'
    category = ADMIN_CATEGORY


class BasketAdmin(ModelView, model=Basket):
    icon = "fa-solid fa-basket-shopping"
    column_list = [Basket.id, Basket.user_id, Basket.price, Basket.status]
    column_searchable_list = [Basket.id, Basket.user_id, Basket.status]
    category = "Shop"


def register_hr_admin_views(admin):
    admin.add_view(UserAdmin)
    admin.add_view(UserAddressAdmin)
    admin.add_view(BasketAdmin)


