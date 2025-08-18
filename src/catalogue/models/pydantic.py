from typing import Optional

from pydantic import (
    BaseModel,
    constr,
)


class ProductModel(BaseModel):
    id: Optional[int]
    title: str
    description: Optional[str]
    short_description: Optional[constr(max_length=20)] # type: ignore
    is_active: bool

    class Config:
        from_attributes = True


class CategoryModel(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: Optional[bool] = True
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True