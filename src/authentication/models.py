from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str = Field(..., min_length=10)
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None
    user_id: int | None = None
    roles: list[str] | None = []
