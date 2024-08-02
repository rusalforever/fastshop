from typing import Generic, List, TypeVar
from pydantic import BaseModel
from src.common.repository.sqlalchemy import BaseSQLAlchemyRepository

T = TypeVar('T')
PType = TypeVar('PType', bound=BaseModel)

class ReadMixin(Generic[PType]):
    def __init__(self, repository: BaseSQLAlchemyRepository[T]):
        self.repository = repository

    async def list(self) -> List[PType]:
        return await self.repository.all()

    async def detail(self, pk: int) -> PType:
        return await self.repository.get(pk=pk)

class WriteMixin(Generic[PType]):
    def __init__(self, repository: BaseSQLAlchemyRepository[T]):
        self.repository = repository

    async def create(self, instance_data: PType) -> PType:
        return await self.repository.create(instance_data)

    async def update(self, pk: int, update_data: PType) -> PType:
        return await self.repository.update(pk, update_data)

    async def delete(self, pk: int):
        await self.repository.delete(pk=pk)

class BaseService(ReadMixin[PType], WriteMixin[PType], Generic[PType]):
    def __init__(self, repository: BaseSQLAlchemyRepository[T]):
        self.repository = repository
        ReadMixin.__init__(self, repository)
        WriteMixin.__init__(self, repository)
