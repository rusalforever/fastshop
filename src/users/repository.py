from typing import Optional

from fastapi import Depends
from sqlalchemy.exc import (
    MultipleResultsFound,
    NoResultFound,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.common.databases.postgres import get_session
from src.common.exceptions.base import (
    ObjectAlreadyExistException,
    ObjectDoesNotExistException,
)
from src.common.repository.sqlalchemy import BaseSQLAlchemyRepository
from src.users.models.database import User


class UserRepository(BaseSQLAlchemyRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def create(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    async def get_by_email(self, email: str) -> Optional[User]:
        statement = select(self.model).where(self.model.email == email)
        result = await self.session.exec(statement)
        try:
            instance = result.one()
        except NoResultFound:
            raise ObjectDoesNotExistException()
        except MultipleResultsFound:
            raise ObjectAlreadyExistException()

        return instance


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session=session)
