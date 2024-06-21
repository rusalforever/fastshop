from src.common.repository.beanie import BaseMongoRepository
from src.reviews.models.mongo import ProductReview


class ProductReviewRepository(BaseMongoRepository[ProductReview]):
    __model__ = ProductReview
