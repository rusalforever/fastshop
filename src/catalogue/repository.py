from beanie import init_beanie, PydanticObjectId, Document
from beanie.odm.operators.update.general import Set
from motor.motor_asyncio import AsyncIOMotorClient
from ..common.databases.mongo_db import AsyncMongoDBClient
from src.base_settings import base_settings
from .models.mongo import ProductAnalytics
from pydantic import BaseModel

class ProductAnalyticsRepository:
    def __init__(self):
        self.client = AsyncMongoDBClient(base_settings.mongo["url"])
        self.database = self.client.get_database()
        self.collection = ProductAnalytics

    async def insert_one(self, product_analytics: ProductAnalytics):
        await product_analytics.insert()

    async def get_all(self):
        return await self.collection.find({}).to_list()

    async def get_by_id(self, product_id: int):
        return await self.collection.find_one(ProductAnalytics.product_id == product_id)

    @staticmethod
    async def init_product_analytics_repository():
        client = AsyncMongoDBClient(base_settings.mongo["url"])
        db = client.get_database()
        await init_beanie(database=db, document_models=[ProductAnalytics])
        return ProductAnalyticsRepository()
