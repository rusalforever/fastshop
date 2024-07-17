from src.common.routes import BaseCrudPrefixes


class UserManagementRoutesPrefixes:
    user: str = '/user'
    user_address: str = '/user/address'


class UserRoutesPrefixes(BaseCrudPrefixes):
    ...


class UserAddressRoutesPrefixes(BaseCrudPrefixes):
    ...
