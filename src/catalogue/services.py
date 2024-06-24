from typing import List, Optional

from fastapi import Depends

from src.catalogue.models.pydantic import ProductModel, CategoryModel
from src.catalogue.repository import (
    ProductRepository,
    get_product_repository, CategoryRepository, get_category_repository,
)
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.service import BaseService


class ProductService(BaseService[ProductModel]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)


def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def get_all_categories(self) -> List[CategoryModel]:
        return await self.repository.all()

    async def get_category(self, category_id: int) -> Optional[CategoryModel]:
        category = await self.repository.get(category_id)
        if not category:
            raise ObjectDoesNotExistException(f"Category with id {category_id} does not exist")
        return category

    async def create_category(self, category: CategoryModel) -> CategoryModel:
        return await self.repository.create(category)

    async def update_category(self, category_id: int, category: CategoryModel) -> Optional[CategoryModel]:
        return await self.repository.update(category_id, category)

    async def delete_category(self, category_id: int) -> bool:
        return await self.repository.delete(category_id)


def get_category_service(repository: CategoryRepository = Depends(get_category_repository)) -> CategoryService:
    return CategoryService(repository)
