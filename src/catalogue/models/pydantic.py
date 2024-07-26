from typing import Optional

from pydantic import BaseModel


class ProductElasticResponse(BaseModel):
    product_id: int
    title: str
    score: float


class ProductCreate(BaseModel):
    title: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    is_active: bool = True

