"""
Provide connection to MongoDB. Default database "casafari".
"""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from src.catalogue.models.mongo import ProductAnalytics
from src.reviews.models.mongo import ProductReview
from src.base_settings import base_settings
from src.common.singleton import SingletonMeta


class AsyncMongoDBClient(AsyncIOMotorClient, metaclass=SingletonMeta):
    """
    Provide singleton client for MongoDB.
    """

    def get_database(self, name=None):
        """
        Returns the default database or the database specified by name.
        """
        return super().get_database(name or base_settings.mongo["default_db"])


async def init_mongo_db():
    client = AsyncMongoDBClient(base_settings.mongo["url"])
    await init_beanie(
        database=client.get_database(),
        document_models=[
            ProductReview,
            ProductAnalytics
        ],
    )
