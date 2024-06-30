from typing import Union, Optional

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


class UserAddressBaseModel(BaseModel):
    user_id: int
    title: str

    class Config:
        from_attributes = True


class UserAddressModel(UserAddressBaseModel):
    city: str
    house: str
    street: str
    floor: Optional[str]
    apartment: Optional[str]
    post_code: Optional[str]
    additional_info: Optional[str]
