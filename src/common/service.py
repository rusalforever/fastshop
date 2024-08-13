from typing import (
    Generic,
    List,
    TypeVar,
    Union,
)

from pydantic import BaseModel

from src.common.repository.beanie import BaseMongoRepository
from src.common.repository.sqlalchemy import BaseSQLAlchemyRepository


T = TypeVar('T')
PType = TypeVar('PType', bound=BaseModel)


class ReadMixin(Generic[PType]):
    """
    Mixin class to provide read operations.
    """
    repository: Union[BaseSQLAlchemyRepository[T, PType], BaseMongoRepository]

    async def list(self) -> List[PType]:
        """
        List all instances of the model.
        """
        return await self.repository.all()

    async def detail(self, pk: Union[int, str]) -> PType:
        """
        Retrieve a single instance of the model by its primary key.
        """
        return await self.repository.get(pk=pk)


class WriteMixin(Generic[PType]):
    """
    Mixin class to provide write operations.
    """
    repository: Union[BaseSQLAlchemyRepository[T, PType], BaseMongoRepository]

    async def create(self, instance_data: PType) -> PType:
        """
        Create a new instance of the model.
        """
        return await self.repository.create(instance_data)

    async def update(self, pk: Union[int, str], update_data: PType) -> PType:
        """
        Update an existing instance of the model by its primary key.
        """
        return await self.repository.update(pk, update_data)

    async def delete(self, pk: Union[int, str]):
        """
        Delete an instance of the model by its primary key.
        """
        await self.repository.delete(pk=pk)


class BaseService(ReadMixin[PType], WriteMixin[PType], Generic[PType]):
    """
    Base service class that provides common read and write operations.
    """
    def __init__(self, repository: Union[BaseSQLAlchemyRepository[T, PType], BaseMongoRepository]):
        self.repository = repository
