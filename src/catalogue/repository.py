from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.catalogue.models.pydantic import ProductModel
from src.catalogue.models.sqlalchemy import Product
from src.common.databases.postgres import (
    get_session,
)
from src.common.repository.sqlalchemy import BaseSQLAlchemyRepository


class ProductRepository(BaseSQLAlchemyRepository[Product, ProductModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Product, pydantic_model=ProductModel, session=session)


def get_product_repository(session: AsyncSession = Depends(get_session)) -> ProductRepository:
    return ProductRepository(session=session)
