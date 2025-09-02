from typing import (
    Annotated,
    Union, List
)

from fastapi import (
    APIRouter,
    Depends,
    status,
    Response
)

from src.common.exceptions.base import ObjectDoesNotExistException
from src.authentication.utils import get_current_user
from src.common.schemas.common import ErrorResponse
from src.users.models.pydantic import (
    UserModel, UserAddressBriefModel, UserAddressDetailModel,
)
from src.users.routes import (
    UserManagementRoutesPrefixes,
    UserRoutesPrefixes,
)
from src.users.services import UserAddressService, get_user_address_service

router = APIRouter(prefix=UserManagementRoutesPrefixes.user)
address_router = APIRouter(prefix=UserManagementRoutesPrefixes.address)


@router.get(
    UserRoutesPrefixes.root,
    responses={
        status.HTTP_200_OK: {'model': UserModel},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[UserModel, ErrorResponse],
)
async def user_detail(
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> Union[UserModel, ErrorResponse]:
    """
    Retrieve user.

    Returns:
        Response with user details.
    """

    return current_user

@address_router.get(
    UserRoutesPrefixes.root,
    responses={
        status.HTTP_200_OK: {'model': UserAddressBriefModel},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}
    },
    status_code=status.HTTP_200_OK,
    response_model=List[UserAddressBriefModel],
)
async def user_addresses_list(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    address_service: Annotated[UserAddressService, Depends(get_user_address_service)],
) -> List[UserAddressBriefModel]:
    addresses = await address_service.get_addresses_list(user_id=current_user.id)
    return [
        UserAddressBriefModel(
            id=address.id,
            title=address.title
        )
        for address in addresses
    ]

@address_router.get(
    UserRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': UserAddressDetailModel},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[UserAddressDetailModel, ErrorResponse],
)
async def user_address_details(
    response: Response,
    address_id: int,
    address_service: Annotated[UserAddressService, Depends(get_user_address_service)],
) -> Union[Response, ErrorResponse]:
    try:
        response = await address_service.get_address_detail(address_id=address_id)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response