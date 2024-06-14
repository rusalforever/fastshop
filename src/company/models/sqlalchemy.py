from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)

from src.common.databases.postgres import Base


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    first_name = Column(String)
    last_name = Column(String)
