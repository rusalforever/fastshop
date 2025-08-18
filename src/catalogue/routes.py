from src.common.routes import BaseCrudPrefixes


class CatalogueRoutesPrefixes:
    product: str = '/product'
    category: str = '/category'


class ProductRoutesPrefixes(BaseCrudPrefixes):
    ...


class CategoryRoutesPrefixes(BaseCrudPrefixes):
    list: str = '/categories'         # GET список категорій
    detail: str = '/categories/{pk}'  # GET деталі категорії
    create: str = '/categories'       # POST створення
    update: str = '/categories/{pk}'  # PUT оновлення
    delete: str = '/categories/{pk}'  # DELETE видалення
