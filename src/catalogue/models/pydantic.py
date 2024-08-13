from typing import Optional
from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    id: Optional[int]
    title: str = Field(..., min_length=1)
    description: Optional[str]
    short_description: Optional[str] = Field(None, max_length=20)
    is_active: bool

    class Config:
        from_attributes = True
