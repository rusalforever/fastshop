from src.common.routes import BaseCrudPrefixes


class CatalogueRoutesPrefixes:
    product: str = '/product'
    additional_products: str = '/additional-products'
    recommended_products: str = '/recommended-products'


class ProductRoutesPrefixes(BaseCrudPrefixes):
    ...


class AdditionalProductsRoutesPrefixes(BaseCrudPrefixes):
    ...


class RecommendedProductsRoutesPrefixes(BaseCrudPrefixes):
    ...
