from typing import (
    Generic,
    List,
    Type,
    TypeVar,
)

from pydantic import BaseModel
from sqlalchemy import (
    delete as sqlalchemy_delete,
    update as sqlalchemy_update,
)
from sqlalchemy.exc import (
    MultipleResultsFound,
    NoResultFound,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.common.exceptions.base import (
    ObjectAlreadyExistException,
    ObjectDoesNotExistException,
)


T = TypeVar('T')
PType = TypeVar('PType', bound=BaseModel)


class BaseSQLAlchemyRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, pk: int) -> PType:
        statement = select(self.model).where(self.model.id == pk)
        result = await self.session.exec(statement)
        try:
            instance = result.one()
        except NoResultFound:
            raise ObjectDoesNotExistException()
        except MultipleResultsFound:
            raise ObjectAlreadyExistException()

        return instance

    async def create(self, instance_data: PType) -> PType:
        instance = self.model(**instance_data.model_dump())
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return self.model.model_validate(instance)

    async def update(self, pk: int, update_data: PType) -> PType:
        await self.session.exec(
            sqlalchemy_update(self.model).where(self.model.id == pk).values(**update_data.model_dump()),
        )
        await self.session.commit()
        return await self.get(pk=pk)

    async def delete(self, pk: int):
        statement = sqlalchemy_delete(self.model).where(self.model.id == pk)
        await self.session.exec(statement)
        await self.session.commit()

    async def all(self) -> List[PType]:
        statement = select(self.model)
        result = await self.session.exec(statement)
        return result.all()

    async def filter(self, **kwargs) -> List[PType]:
        statement = select(self.model).filter_by(**kwargs)
        result = await self.session.exec(statement)
        return result.all()
