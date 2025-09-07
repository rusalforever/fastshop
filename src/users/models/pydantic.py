from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, EmailStr

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

class UserAddressBase(BaseModel):
    title: Optional[str] = None
    city: str
    street: str
    house: str
    apartment: Optional[str] = None
    post_code: Optional[str] = None
    floor: Optional[str] = None
    additional_info: Optional[str] = None


class UserAddressCreate(UserAddressBase):
    pass


class UserAddressModel(UserAddressBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class UserAddressShort(BaseModel):
    id: int
    title: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserAddressDetail(UserAddressBase):
    id: int

    model_config = ConfigDict(from_attributes=True)