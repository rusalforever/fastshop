from beanie import Document
from datetime import datetime

class ProductAnalytics(Document):
    product_id: int
    timestamp: datetime

    class Settings:
        collection = "product_analytics"
