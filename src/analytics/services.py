from datetime import datetime, timezone
from typing import Annotated, Optional

from fastapi import Depends

from src.common.service import BaseService
from src.analytics.models.mongo import ProductAnalytics
from src.analytics.repositories import ProductAnalyticsRepository


class ProductAnalyticsService(BaseService):
    def __init__(
        self,
        repository: Annotated[ProductAnalyticsRepository, Depends(ProductAnalyticsRepository)],
    ):
        super().__init__(repository=repository)

    async def record_visit(self, product_id: int, timestamp: Optional[datetime] = None) -> ProductAnalytics:
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        instance = ProductAnalytics(product_id=product_id, timestamp=timestamp)
        return await self.repository.create(instance=instance)
