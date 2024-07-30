from typing import List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.catalogue.models.database import Product
from src.common.databases.postgres import get_session
from src.common.repository.sqlalchemy import BaseSQLAlchemyRepository
from sqlmodel import select, or_


class ProductRepository(BaseSQLAlchemyRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Product, session=session)



    async def filter(self, query: str) -> List[Product]:
        statement = select(self.model).where(
            or_(
                self.model.title.ilike(f'%{query}%'),
                self.model.short_description.ilike(f'%{query}%'),
                self.model.description.ilike(f'%{query}%')
            )
        )
        result = await self.session.exec(statement)
        return result.all()


def get_product_repository(session: AsyncSession = Depends(get_session)) -> ProductRepository:
    return ProductRepository(session=session)
