from typing import Union, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Union[int, None] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone_number: str


class UserWithPassword(UserModel):
    hashed_password: str
