from fastapi import Depends

from src.catalogue.models.pydantic import ProductModel
from src.catalogue.repository import (
    ProductRepository,
    get_product_repository,
)
from src.catalogue.models.pydantic import CategoryModel
from src.catalogue.repository import CategoryRepository, get_category_repository
from src.common.service import BaseService


class ProductService(BaseService[ProductModel]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)

def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)


class CategoryService(BaseService[CategoryModel]):
    def __init__(self, repository: CategoryRepository):
        super().__init__(repository)

    async def get_subcategories(self, parent_id: int):
        return await self.repository.list(filters={"parent_id": parent_id})

def get_category_service(repo: CategoryRepository = Depends(get_category_repository)) -> CategoryService:
    return CategoryService(repository=repo)