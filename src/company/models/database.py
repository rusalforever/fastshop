from typing import Optional

from sqlmodel import (
    Field,
    SQLModel,
)


class Company(SQLModel, table=True):
    __tablename__ = 'company'

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    phone_number: str
    hashed_password: str
    is_admin: bool = False
    is_staff: bool = False
    is_active: bool = True
    first_name: str
    last_name: str
