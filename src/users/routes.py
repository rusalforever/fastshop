from src.common.routes import BaseCrudPrefixes


class UserManagementRoutesPrefixes:
    user: str = '/user'
    address: str = '/address'


class UserRoutesPrefixes(BaseCrudPrefixes):
    ...
