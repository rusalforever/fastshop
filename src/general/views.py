"""
Provide status views.
"""
from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from src.common.schemas.common import DetailsResponse
from src.general.routes import GeneralRoutesPrefixes
from src.users.dependencies import get_current_user

from src.users.models.pydantic import (
    UserModel,
    UserAddressShort,
    UserAddressDetail,
)
from src.users.services import (
    UserAddressService,
    get_user_address_service,
)


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

@router.get("/", response_model=List[UserAddressShort])
async def list_addresses(
    current_user: UserModel = Depends(get_current_user),
    service: UserAddressService = Depends(get_user_address_service),
):
    addresses = await service.get_user_addresses(user_id=current_user.id)
    return [UserAddressShort.model_validate(addr) for addr in addresses]


@router.get("/{address_id}", response_model=UserAddressDetail)
async def address_detail(
    address_id: int,
    current_user: UserModel = Depends(get_current_user),
    service: UserAddressService = Depends(get_user_address_service),
):
    address = await service.get_user_address_detail(user_id=current_user.id, address_id=address_id)
    if not address:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to access this address")
    return UserAddressDetail.model_validate(address)