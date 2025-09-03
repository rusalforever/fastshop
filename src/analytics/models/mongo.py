from datetime import datetime, timezone

from beanie import Document
from pydantic import BaseModel


class BaseProductAnalytics(BaseModel):
    product_id: int
    timestamp: datetime


class ProductAnalytics(Document, BaseProductAnalytics):
    class Settings:
        name = 'productAnalytics'

    @classmethod
    def new_visit(cls, product_id: int, timestamp: datetime | None = None) -> "ProductAnalytics":
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        return cls(product_id=product_id, timestamp=timestamp)
