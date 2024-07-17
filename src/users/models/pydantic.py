from typing import Union

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


class UserAddressTitle(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str


class UserAddressModel(UserAddressTitle):
    city: str
    street: str
    house: str
    apartment: str
    post_code: str
    floor: str
    additional_info: str
