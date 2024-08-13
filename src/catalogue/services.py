from fastapi import Depends
from .repository import ProductRepository, get_product_repository, ProductAnalyticsRepository
from .models.pydantic import ProductModel
from ..common.service import BaseService
from datetime import datetime
from .repository import ProductAnalyticsRepository
from .models.mongo import ProductAnalytics

class ProductService(BaseService[ProductModel]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)

def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)

class ProductAnalyticsService:
    def __init__(self, product_analytics_repo: ProductAnalyticsRepository):
        self.product_analytics_repo = product_analytics_repo

    async def record_product_visit(self, product_id: int):
        timestamp = datetime.utcnow()
        product_analytics = ProductAnalytics(product_id=product_id, timestamp=timestamp)
        await self.product_analytics_repo.insert_one(product_analytics)