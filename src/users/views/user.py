from typing import (
    Annotated,
    Union,
)

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from src.authentication.utils import get_current_user
from src.common.schemas.common import ErrorResponse
from src.users.models.pydantic import (
    UserModel,
)
from src.users.routes import (
    UserManagementRoutesPrefixes,
    UserRoutesPrefixes,
)


router = APIRouter(prefix=UserManagementRoutesPrefixes.user)


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
