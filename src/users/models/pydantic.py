from typing import Union
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Union[int, None] = None
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str


class UserWithPassword(UserModel):
    hashed_password: str


class UserAddressListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: Optional[str] = None


class UserAddressDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: Optional[str] = None
    city: str
    street: str
    house: str
    apartment: Optional[str] = None
    post_code: Optional[str] = None
    floor: Optional[str] = None
    additional_info: Optional[str] = None