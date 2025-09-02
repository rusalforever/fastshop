from typing import Annotated, Union

from fastapi import APIRouter, Depends, Response, status

from src.authentication.utils import get_current_user
from src.common.schemas.common import ErrorResponse
from src.users.models.pydantic import (
    UserModel,
    UserAddressDetail,
    UserAddressListItem,
)
from src.users.routes import UserManagementRoutesPrefixes, UserRoutesPrefixes
from src.users.services import get_user_address_service
from src.common.exceptions.base import ObjectDoesNotExistException


router = APIRouter(prefix=f"{UserManagementRoutesPrefixes.user}{UserManagementRoutesPrefixes.addresses}")


@router.get(
    UserRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[UserAddressListItem],
)
async def user_address_list(
    current_user: Annotated[UserModel, Depends(get_current_user)],
    service: Annotated[get_user_address_service, Depends()],
) -> list[UserAddressListItem]:
    return await service.list_by_user(user_id=current_user.id)


@router.get(
    UserRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': UserAddressDetail},
        status.HTTP_403_FORBIDDEN: {'model': ErrorResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[UserAddressDetail, ErrorResponse],
)
async def user_address_detail(
    response: Response,
    pk: int,
    current_user: Annotated[UserModel, Depends(get_current_user)],
    service: Annotated[get_user_address_service, Depends()],
) -> Union[UserAddressDetail, ErrorResponse]:
    instance = await service.get_sqlalchemy(pk=pk)
    if instance is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message="Address does not exist")

    if instance.user_id != current_user.id:
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(message="You do not have permission to access this address")

    try:
        return await service.detail(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)
