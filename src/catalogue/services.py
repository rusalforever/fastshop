from fastapi import Depends

from src.catalogue.models.database import Product
from src.catalogue.repository import (
    ProductRepository,
    get_product_repository,
)
from src.common.service import BaseService


class ProductService(BaseService[Product]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)


def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)
