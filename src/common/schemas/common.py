from pydantic import BaseModel


class DetailsResponse(BaseModel):
    details: str


class ErrorResponse(BaseModel):
    message: str
