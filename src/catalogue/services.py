from fastapi import Depends

from src.catalogue.models.database import Product, AdditionalProducts, RecommendedProducts
from src.catalogue.repository import (
    ProductRepository,
    get_product_repository,
    AdditionalProductsRepository,
    RecommendedProductsRepository
)
from src.common.service import BaseService


class ProductService(BaseService[Product]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)


def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)


class AdditionalProductsService:
    def __init__(self, repository: AdditionalProductsRepository):
        self.repository = repository

    def add_additional_product(self, primary_id: int, additional_id: int):
        additional_product = AdditionalProducts(primary_id=primary_id, additional_id=additional_id)
        return self.repository.add(additional_product)

    def get_additional_products(self, primary_id: int):
        return self.repository.get_by_primary_id(primary_id)

    def update_additional_product(self, additional_product: AdditionalProducts):
        return self.repository.update(additional_product)

    def delete_additional_product(self, additional_product: AdditionalProducts):
        return self.repository.delete(additional_product)


class RecommendedProductsService:
    def __init__(self, repository: RecommendedProductsRepository):
        self.repository = repository

    def add_recommended_product(self, primary_id: int, recommended_id: int):
        recommended_product = RecommendedProducts(primary_id=primary_id, recommended_id=recommended_id)
        return self.repository.add(recommended_product)

    def get_recommended_products(self, primary_id: int):
        return self.repository.get_by_primary_id(primary_id)

    def update_recommended_product(self, recommended_product: RecommendedProducts):
        return self.repository.update(recommended_product)

    def delete_recommended_product(self, recommended_product: RecommendedProducts):
        return self.repository.delete(recommended_product)
