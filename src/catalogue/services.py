from fastapi import Depends

from src.catalogue.models.pydantic import ProductModel
from src.catalogue.repository import (
    ProductRepository,
    get_product_repository,
)
from src.common.service import BaseService


class ProductService(BaseService[ProductModel]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)


def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)
