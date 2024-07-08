from typing import List
from fastapi import Depends
from src.catalogue.models.database import Product, AdditionalProducts, RecommendedProducts
from src.catalogue.repository import (
    ProductRepository, get_product_repository,
    AdditionalProductsRepository, get_additional_products_repository,
    RecommendedProductsRepository, get_recommended_products_repository,
)
from src.common.service import BaseService


class ProductService(BaseService[Product]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)


def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)


class AdditionalProductsService(BaseService[AdditionalProducts]):
    def __init__(self, repository: AdditionalProductsRepository):
        super().__init__(repository)

    async def add_additional_product(self, primary_id: int, additional_id: int) -> AdditionalProducts:
        additional_product = AdditionalProducts(primary_id=primary_id, additional_id=additional_id)
        return await self.repository.create(instance_data=additional_product)

    async def update_additional_product(self, primary_id: int, additional_id: int) -> AdditionalProducts:
        # Assuming update_data is passed to update method
        update_data = AdditionalProducts(primary_id=primary_id, additional_id=additional_id)
        return await self.repository.update(pk=primary_id, update_data=update_data)

    async def remove_additional_product(self, primary_id: int, additional_id: int):
        await self.repository.delete(pk=primary_id, additional_id=additional_id)

    async def list_additional_products(self, primary_id: int) -> List[AdditionalProducts]:
        return await self.repository.filter(primary_id=primary_id)


def get_additional_products_service(
        repo: AdditionalProductsRepository = Depends(get_additional_products_repository)) -> AdditionalProductsService:
    return AdditionalProductsService(repository=repo)


class RecommendedProductsService(BaseService[RecommendedProducts]):
    def __init__(self, repository: RecommendedProductsRepository):
        super().__init__(repository)

    async def add_recommended_product(self, primary_id: int, recommended_id: int) -> RecommendedProducts:
        recommended_product = RecommendedProducts(primary_id=primary_id, recommended_id=recommended_id)
        return await self.repository.create(instance_data=recommended_product)

    async def update_recommended_product(self, primary_id: int, recommended_id: int) -> RecommendedProducts:
        update_data = RecommendedProducts(primary_id=primary_id, recommended_id=recommended_id)
        return await self.repository.update(pk=primary_id, update_data=update_data)

    async def remove_recommended_product(self, primary_id: int, recommended_id: int):
        await self.repository.delete(pk=primary_id, recommended_id=recommended_id)

    async def list_recommended_products(self, primary_id: int) -> List[RecommendedProducts]:
        return await self.repository.filter(primary_id=primary_id)


def get_recommended_products_service(
        repo: RecommendedProductsRepository = Depends(get_recommended_products_repository)) -> RecommendedProductsService:
    return RecommendedProductsService(repository=repo)
