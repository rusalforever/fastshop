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

class UserAddressModel(BaseModel):
    """UserAddress Pydantic model matching the SQLAlchemy model."""
    model_config = ConfigDict(from_attributes=True)

    id: Union[int, None] = None
    user_id: int
    title: Optional[str] = None
    city: str
    street: str
    house: str
    apartment: Optional[str] = None
    post_code: Optional[str] = None
    floor: Optional[str] = None
    additional_info: Optional[str] = None

class UserAddressBriefModel(BaseModel):
    """Brief model for API list responses (id + title only)"""
    model_config = ConfigDict(from_attributes=True)
    id: Union[int, None] = None
    title: Optional[str] = None

class UserAddressDetailModel(BaseModel):
    """Detail model for API responses (all fields except user_id)"""
    model_config = ConfigDict(from_attributes=True)
    id: Union[int, None] = None
    title: Optional[str] = None
    city: str
    street: str
    house: str
    apartment: Optional[str] = None
    post_code: Optional[str] = None
    floor: Optional[str] = None
    additional_info: Optional[str] = None
