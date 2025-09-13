from fastapi import Depends

from src.catalogue.models.database import Product, AdditionalProducts, RecommendedProducts
from src.catalogue.repository import (
    ProductRepository,
    get_product_repository,
    AdditionalProductsRepository,
    RecommendedProductsRepository,
)
from src.common.service import BaseService
from sqlmodel import Session


class ProductService(BaseService[Product]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)


def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)

class AdditionalProductsService:
    def __init__(self, session: Session):
        self.repo = AdditionalProductsRepository(session)

    def list_for_product(self, primary_id: int):
        """Список додаткових товарів для конкретного продукту"""
        return self.repo.get_all_by_primary(primary_id)

    def add_relation(self, primary_id: int, additional_id: int):
        obj = AdditionalProducts(primary_id=primary_id, additional_id=additional_id)
        return self.repo.create(obj)

    def update_relation(self, id_: int, **kwargs):
        """Оновлення зв’язку (наприклад, змінити additional_id)"""
        db_obj = self.repo.get_by_id(id_)
        if not db_obj:
            return None
        return self.repo.update(db_obj, **kwargs)

    def remove_relation(self, id_: int):
        db_obj = self.repo.get_by_id(id_)
        if db_obj:
            self.repo.delete(db_obj)
            return True
        return False

class RecommendedProductsService:
    def __init__(self, session: Session):
        self.repo = RecommendedProductsRepository(session)

    def list_all(self):
        return self.repo.get_all()

    def get(self, id_: int):
        return self.repo.get_by_id(id_)

    def add_relation(self, primary_id: int, recommended_id: int):
        obj = RecommendedProducts(primary_id=primary_id, recommended_id=recommended_id)
        return self.repo.create(obj)

    def remove_relation(self, id_: int):
        return self.repo.delete(id_)