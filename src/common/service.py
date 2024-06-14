from typing import (
    Generic,
    List,
    TypeVar,
)

from pydantic import BaseModel

from src.common.repository.sqlalchemy import BaseSQLAlchemyRepository


T = TypeVar('T')
PType = TypeVar('PType', bound=BaseModel)


class ReadMixin:
    async def list(self) -> List[PType]:
        return await self.repository.all()

    async def detail(self, pk: int) -> PType:
        return await self.repository.get(pk=pk)


class WriteMixin:
    async def create(self, instance_data: PType) -> PType:
        return await self.repository.create(instance_data)

    async def update(self, pk: int, update_data: PType) -> PType:
        return await self.repository.update(id, update_data)

    async def delete(self, pk: int):
        await self.repository.delete(pk=pk)


class BaseService(ReadMixin, WriteMixin, Generic[PType]):
    def __init__(self, repository: BaseSQLAlchemyRepository[T, PType]):
        self.repository = repository
