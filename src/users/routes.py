from src.common.routes import BaseCrudPrefixes


class UserManagementRoutesPrefixes:
    user: str = '/user'
    addresses: str = '/addresses'


class UserRoutesPrefixes(BaseCrudPrefixes):
    ...
