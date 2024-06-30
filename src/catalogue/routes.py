from src.common.routes import BaseCrudPrefixes


class CatalogueRoutesPrefixes:
    product: str = '/product'
    addresses: str = '/addresses'


class ProductRoutesPrefixes(BaseCrudPrefixes):
    ...
