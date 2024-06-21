from typing import (
    Generic,
    Optional,
    TypeVar,
)

from beanie import Document
from pydantic import BaseModel

from src.common.exceptions.base import ObjectDoesNotExistException


T = TypeVar('T', bound=Document)


class BaseMongoRepository(Generic[T]):
    """
    Base class for MongoDB repositories.
    """

    __model__: type[T] = None

    async def get(self, pk: Optional[str] = None, **kwargs) -> T:
        if pk is not None:
            instance = await self.__model__.get(document_id=pk)
        else:
            instance = await self.__model__.find_one(kwargs)

        if not instance:
            raise ObjectDoesNotExistException()

        return instance

    async def create(self, instance: BaseModel) -> T:
        if not isinstance(instance, Document):
            instance = self.__model__(**instance.model_dump())

        return await self.__model__.insert_one(instance)

    async def update(self, pk, **kwargs) -> T:
        instance = await self.get(pk=pk)

        return await instance.set(expression=kwargs)

    async def all(self) -> list[T]:  # noqa: A003
        return await self.__model__.find().to_list()

    async def filter(self, **kwargs) -> list[T]:  # noqa: A003
        return await self.__model__.find(**kwargs).to_list()

    async def delete(self, pk: str):
        instance = await self.get(document_id=pk)

        return await instance.delete()
