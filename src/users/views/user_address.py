from typing import (
    Annotated,
    Union,
)

from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
)

from src.authentication.utils import get_current_user
from src.common.schemas.common import ErrorResponse
from src.users.models.pydantic import (
    UserAddressTitle, UserAddressModel, UserModel
)
from src.users.services import get_user_address_service
from src.users.routes import (
    UserManagementRoutesPrefixes,
    UserAddressRoutesPrefixes,
)
from src.common.exceptions.base import ObjectDoesNotExistException



router = APIRouter(prefix=UserManagementRoutesPrefixes.user_address)


@router.get(
    UserAddressRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[UserAddressTitle],
)
async def user_addresses(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    service: Annotated[get_user_address_service, Depends()],
) -> list[UserAddressTitle]:
    """
        Retrieve list user addresses for current user.

        Returns:
            Response with user addresses for current user.
    """
    return await service.get_user_addresses(current_user.id)


@router.get(
    UserAddressRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': UserAddressModel},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[UserAddressModel, ErrorResponse],
)
async def product_detail(
    response: Response,
    pk: int,
    service: Annotated[get_user_address_service, Depends()],
) -> Union[Response, ErrorResponse]:
    """
    Retrieve user address.

    Returns:
        Response with user address details.
    """
    try:
        response = await service.get_user_address(pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response
