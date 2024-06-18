from typing import Optional

from fastapi import Depends

from src.authentication.security import verify_password
from src.common.service import BaseService
from src.users.models.pydantic import (
    UserModel,
)
from src.users.repository import (
    UserRepository,
    get_user_repository,
)


class UserService(BaseService[UserModel]):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    async def get_by_email(self, email: str):
        return await self.repository.get_by_email(email=email)

    async def authenticate(self, email: str, password: str) -> Optional[UserModel]:
        user = await self.get_by_email(email=email)

        if user is None or not verify_password(plain_password=password, hashed_password=user.hashed_password):
            return None
        else:
            return user


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repository=repo)
