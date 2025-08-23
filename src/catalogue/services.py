from fastapi import Depends
from sqlalchemy import update as sqlalchemy_update

from src.catalogue.models.pydantic import ProductModel, CategoryModel
from src.catalogue.repository import (
    ProductRepository,
    get_product_repository,
    CategoryRepository,
    get_category_repository,
)
from src.common.service import BaseService


class ProductService(BaseService[ProductModel]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)


def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)


class CategoryService(BaseService[CategoryModel]):
    def __init__(self, repository: CategoryRepository):
        super().__init__(repository)

    async def list_active(self) -> list[CategoryModel]:
        return await self.repository.filter(is_active=True)

    async def list_subcategories(self, parent_id: int) -> list[CategoryModel]:
        return await self.repository.filter(parent_id=parent_id)

    async def update(self, pk: int, update_data: CategoryModel) -> CategoryModel:
        if update_data.parent_id is not None and update_data.parent_id == pk:
            raise ValueError("Category cannot be parent of itself.")

        values = update_data.model_dump(exclude={"id"})
        await self.repository.session.execute(
            sqlalchemy_update(self.repository.model).where(self.repository.model.id == pk).values(**values)
        )
        await self.repository.session.commit()
        return await self.repository.get(pk=pk)


def get_category_service(repo: CategoryRepository = Depends(get_category_repository)) -> CategoryService:
    return CategoryService(repository=repo)
