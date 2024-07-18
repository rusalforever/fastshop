import datetime
import uuid
from beanie import Document
from pydantic import (
    BaseModel,
    Field,
)


class BaseProductAnalytics(BaseModel):
    product_id: int
    timestamp: datetime.datetime


class ProductAnalytics(Document, BaseProductAnalytics):

    class Settings:
        name = "productAnalytics"
