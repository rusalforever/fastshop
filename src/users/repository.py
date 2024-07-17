from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.common.databases.postgres import get_session
from src.common.repository.sqlalchemy import BaseSQLAlchemyRepository
from src.users.models.pydantic import (
    UserModel,
    UserWithPassword,
    UserAddressTitle,
    UserAddressModel,
)
from src.users.models.sqlalchemy import User, UserAddress
from src.common.exceptions.base import ObjectDoesNotExistException


class UserRepository(BaseSQLAlchemyRepository[User, UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, pydantic_model=UserModel, session=session)

    async def create(self, *args, **kwargs):
        raise NotImplementedError

    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    async def get_by_email(self, email: str) -> Optional[UserWithPassword]:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return None

        return UserWithPassword.model_validate(user)


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session=session)


class UserAddressRepository(BaseSQLAlchemyRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(model=UserAddress, pydantic_model=UserAddressTitle, session=session)

    async def get_by_user_id(self, user_id: int) -> list[UserAddressTitle]:
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        res = []
        for row in result.scalars().all():
            res.append(UserAddressTitle.model_validate(row))
        return res

    async def get_by_id(self, id: int) -> Optional[UserAddressModel]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        user_address = result.scalar_one_or_none()
        if not user_address:
            raise ObjectDoesNotExistException()

        return UserAddressModel.model_validate(user_address)

def get_user_address_repository(session: AsyncSession = Depends(get_session)):
    return UserAddressRepository(session=session)
