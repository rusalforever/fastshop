from fastapi import Depends

from src.catalogue.models.database import Product, AdditionalProducts, RecommendedProducts
from src.catalogue.repository import (
    ProductRepository,
    AdditionalProductsRepository,
    RecommendedProductsRepository,
    get_product_repository,
    get_additional_products_repository,
    get_recommended_products_repository,
)
from src.common.service import BaseService


class ProductService(BaseService[Product]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)


class AdditionalProductsService(BaseService[AdditionalProducts]):
    def __init__(self, repository: AdditionalProductsRepository):
        super().__init__(repository)


class RecommendedProductsService(BaseService[RecommendedProducts]):
    def __init__(self, repository: RecommendedProductsRepository):
        super().__init__(repository)

def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)


def get_additional_products_service(
        repo: AdditionalProductsRepository = Depends(get_additional_products_repository)
) -> AdditionalProductsService:
    return AdditionalProductsService(repository=repo)


def get_recommended_products_service(
        repo: RecommendedProductsRepository = Depends(get_recommended_products_repository)
) -> RecommendedProductsService:
    return RecommendedProductsService(repository=repo)
