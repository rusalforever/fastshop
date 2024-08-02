from datetime import datetime

from elasticsearch.exceptions import ConnectionError
from fastapi import Depends

from src.base_settings import base_settings
from src.catalogue.models.database import Product, Category
from src.catalogue.repository import (
    ProductRepository,
    CategoryRepository,
    get_product_repository,
    get_category_repository
)
from src.catalogue.utils import ProductElasticManager
from src.common.enums import TaskStatus
from src.common.service import BaseService
from src.general.schemas.task_status import TaskStatusModel
from src.common.databases.redis import get_redis_client


class ProductService(BaseService[Product]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)

    @staticmethod
    async def search(keyword: str):
        result = await ProductElasticManager().search_product(keyword=keyword)
        return result

    async def update_search_index(self, uuid):
        products = await self.list()

        try:
            await ProductElasticManager().update_index(products=products)
        except ConnectionError as exc:
            await TaskStatusModel(uuid=uuid, status=TaskStatus.ERROR, details=str(exc)).save_to_redis()

        await TaskStatusModel(
            uuid=uuid,
            status=TaskStatus.DONE,
            done_at=datetime.utcnow().strftime(base_settings.date_time_format),
        ).save_to_redis()


def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)


class CategoryService(BaseService[Category]):
    def __init__(self, repository: CategoryRepository, redis_client):
        super().__init__(repository)
        self.redis_client = redis_client

    async def update_category_index(self):
        pass

    def get_index_status(self):
        return "status"

def get_category_service(repo: CategoryRepository = Depends(get_category_repository), redis_client = Depends(get_redis_client)) -> CategoryService:
    return CategoryService(repository=repo, redis_client=redis_client)
