from typing import List, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.common.databases.postgres import get_session
from src.common.repository.sqlalchemy import BaseSQLAlchemyRepository
from src.users.models.pydantic import (
    UserModel,
    UserWithPassword,
    UserAddressDetail,
    UserAddressListItem,
)
from src.users.models.sqlalchemy import User, UserAddress


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


class UserAddressRepository(BaseSQLAlchemyRepository[UserAddress, UserAddressDetail]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=UserAddress, pydantic_model=UserAddressDetail, session=session)

    async def list_by_user(self, user_id: int) -> List[UserAddressListItem]:
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        instances = result.scalars().all()
        return [UserAddressListItem.model_validate(instance) for instance in instances]

    async def get_sqlalchemy(self, pk: int) -> Optional[UserAddress]:
        stmt = select(self.model).where(self.model.id == pk)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


def get_user_address_repository(session: AsyncSession = Depends(get_session)) -> UserAddressRepository:
    return UserAddressRepository(session=session)
