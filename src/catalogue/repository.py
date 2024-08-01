from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session, select

from src.catalogue.models.database import Product, AdditionalProducts, RecommendedProducts
from src.common.databases.postgres import get_session
from src.common.repository.sqlalchemy import BaseSQLAlchemyRepository


class ProductRepository(BaseSQLAlchemyRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Product, session=session)


def get_product_repository(session: AsyncSession = Depends(get_session)) -> ProductRepository:
    return ProductRepository(session=session)


class AdditionalProductsRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, additional_product: AdditionalProducts):
        self.session.add(additional_product)
        self.session.commit()
        self.session.refresh(additional_product)
        return additional_product

    def get_by_primary_id(self, primary_id: int):
        return self.session.exec(select(AdditionalProducts).where(AdditionalProducts.primary_id == primary_id)).all()

    def update(self, additional_product: AdditionalProducts):
        self.session.add(additional_product)
        self.session.commit()
        return additional_product

    def delete(self, additional_product: AdditionalProducts):
        self.session.delete(additional_product)
        self.session.commit()


class RecommendedProductsRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, recommended_product: RecommendedProducts):
        self.session.add(recommended_product)
        self.session.commit()
        self.session.refresh(recommended_product)
        return recommended_product

    def get_by_primary_id(self, primary_id: int):
        return self.session.exec(select(RecommendedProducts).where(RecommendedProducts.primary_id == primary_id)).all()

    def update(self, recommended_product: RecommendedProducts):
        self.session.add(recommended_product)
        self.session.commit()
        return recommended_product

    def delete(self, recommended_product: RecommendedProducts):
        self.session.delete(recommended_product)
        self.session.commit()
