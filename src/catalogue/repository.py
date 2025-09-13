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

    def get_all_by_primary(self, primary_id: int):
        return self.session.exec(
            select(AdditionalProducts).where(AdditionalProducts.primary_id == primary_id)
        ).all()

    def get_by_id(self, id_: int):
        return self.session.get(AdditionalProducts, id_)

    def create(self, obj: AdditionalProducts):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, db_obj: AdditionalProducts, **kwargs):
        for k, v in kwargs.items():
            setattr(db_obj, k, v)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: AdditionalProducts):
        self.session.delete(db_obj)
        self.session.commit()

class RecommendedProductsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.exec(select(RecommendedProducts)).all()

    def get_by_id(self, id_: int):
        return self.session.get(RecommendedProducts, id_)

    def create(self, obj_in: RecommendedProducts) -> RecommendedProducts:
        self.session.add(obj_in)
        self.session.commit()
        self.session.refresh(obj_in)
        return obj_in

    def delete(self, id_: int):
        db_obj = self.get_by_id(id_)
        if db_obj:
            self.session.delete(db_obj)
            self.session.commit()
            return True
        return False