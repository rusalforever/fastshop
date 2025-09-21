from typing import (
    Annotated,
    Union,
)

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Response,
    status,
)

from src.catalogue.models.database import Category
from src.catalogue.routes import (
    CatalogueRoutesPrefixes,
    CategoryRoutesPrefixes,
)
from src.catalogue.services import get_category_service
from src.common.enums import TaskStatus
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse
from src.general.schemas.task_status import TaskStatusModel


router = APIRouter(prefix=CatalogueRoutesPrefixes.category)


@router.get(
    CategoryRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[Category],
)
async def category_list(category_service: Annotated[get_category_service, Depends()]) -> list[Category]:
    """
    Get list of categories.

    Returns:
        Response with list of categories.
    """
    return await category_service.list()


@router.get(
    CategoryRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': Category},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[Category, ErrorResponse],
)
async def category_detail(
    response: Response,
    pk: int,
    service: Annotated[get_category_service, Depends()],
) -> Union[Response, ErrorResponse]:
    """
    Retrieve category.

    Returns:
        Response with category details.
    """
    try:
        response = await service.detail(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response


@router.get(
    CategoryRoutesPrefixes.search,
    status_code=status.HTTP_200_OK,
)
async def search(
    keyword: str,
    service: Annotated[get_category_service, Depends()],
):
    """
    Search categories.

    Returns:
        Response with categories.
    """
    response = await service.search(keyword=keyword)

    return response


@router.post(
    CategoryRoutesPrefixes.update_index,
    status_code=status.HTTP_200_OK,
)
async def update_elastic(
    background_tasks: BackgroundTasks,
    service: Annotated[get_category_service, Depends()],
):
    """
    Update categories index.

    Returns:
        Task status.
    """
    status_model = await TaskStatusModel(status=TaskStatus.IN_PROGRESS).save_to_redis()

    background_tasks.add_task(service.update_category_index, status_model.uuid)

    return await TaskStatusModel().get_from_redis(uuid=status_model.uuid)