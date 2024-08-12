from fastapi import Depends

from src.catalogue.models.pydantic import ProductModel, CategoryModel
from src.catalogue.repository import (
    ProductRepository,
    get_product_repository,
    CategoryRepository,
    get_category_repository,
)
from src.common.service import BaseService

class ProductService(BaseService[ProductModel]):
    def init(self, repository: ProductRepository):
        super().init(repository)

def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)


class CategoryService(BaseService[CategoryModel]):
    def init(self, repository: CategoryRepository):
        super().init(repository)


def get_category_service(
        repo: CategoryRepository = Depends(get_category_repository)
) -> CategoryService:
    return CategoryService(repository=repo)
