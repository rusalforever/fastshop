"""
Provide status views.
"""
from fastapi import (
    APIRouter,
    status,
)

from src.common.schemas.common import DetailsResponse
from src.general.routes import GeneralRoutesPrefixes


router = APIRouter()


@router.get(
    GeneralRoutesPrefixes.health_check,
    tags=['Status'],
    response_model=DetailsResponse,
    status_code=status.HTTP_200_OK,
)
def health_check() -> DetailsResponse:
    """
    Health check endpoint.

    Returns:
        Response showing whether server is alive.
    """
    return DetailsResponse(details='UP')
