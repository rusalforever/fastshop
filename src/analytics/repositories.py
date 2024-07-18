from src.common.repository.beanie import BaseMongoRepository
from src.analytics.models.mongodb import ProductAnalytics


class ProductAnalyticsRepository(BaseMongoRepository[ProductAnalytics]):
    __model__ = ProductAnalytics
