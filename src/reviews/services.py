from typing import Annotated, List, Optional

from fastapi import Depends

from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.service import BaseService
from src.reviews.models.mongo import (
    ProductReview,
    Reply,
)
from src.reviews.repositories import ProductReviewRepository


class ProductReviewService(BaseService[ProductReview]):
    def __init__(
        self,
        repository: Annotated[ProductReviewRepository, Depends(ProductReviewRepository)],
    ):
        super().__init__(repository=repository)

    def __build_reply_tree(self, parent_id: Optional[str], replies: List[Reply]) -> List[Reply]:
        """
        Recursively builds a tree of replies for a given parent ID.
        """
        tree = []
        for reply in replies:
            if reply.to_reply == parent_id:
                reply.replies = self.__build_reply_tree(reply.id, replies)
                tree.append(reply)
        return tree

    async def detail_with_replies(self, pk: str) -> ProductReview:
        """
        Retrieves a product review along with its reply tree.
        Raises an ObjectDoesNotExistException if the review does not exist.
        """
        review = await self.repository.get(pk=pk)
        if not review:
            raise ObjectDoesNotExistException(f"Product review with id {pk} does not exist.")

        review.replies = self.__build_reply_tree(parent_id=None, replies=review.replies)
        return review

    async def add_reply(self, pk: str, reply: Reply) -> ProductReview:
        """
        Adds a reply to a product review.
        Raises an ObjectDoesNotExistException if the review does not exist.
        """
        review = await self.repository.get(pk=pk)
        if not review:
            raise ObjectDoesNotExistException(f"Product review with id {pk} does not exist.")

        review.replies.append(reply.model_dump())
        return await review.save()
