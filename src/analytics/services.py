from datetime import datetime
from typing import Annotated
from fastapi import Depends
from src.analytics.repositories import ProductAnalyticsRepository
from src.common.service import BaseService
from src.analytics.models.mongodb import ProductAnalytics


class ProductAnalyticsService(BaseService):
    def __init__(
            self,
            repository: Annotated[
                ProductAnalyticsRepository, Depends(ProductAnalyticsRepository)],
    ):
        super().__init__(repository=repository)

    async def save_product_opened(self, product_id: int):
        timestamp = datetime.utcnow()
        analytics = ProductAnalytics(product_id=product_id, timestamp=timestamp)
        await self.repository.create(analytics)
