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
from uuid import uuid4

from src.catalogue.models.database import Product
from src.catalogue.routes import (
    CatalogueRoutesPrefixes,
    ProductRoutesPrefixes,
)
from src.catalogue.services import get_product_service, ProductService, get_category_service, CategoryService
from src.common.enums import TaskStatus
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse
from src.general.schemas.task_status import TaskStatusModel

router = APIRouter(prefix=CatalogueRoutesPrefixes.product)


@router.get(
    ProductRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[Product],
)
async def product_list(service: Annotated[ProductService, Depends(get_product_service)]) -> list[Product]:
    """
    Get list of products.

    Returns:
        Response with list of products.
    """
    return await service.list()


@router.get(
    ProductRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': Product},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[Product, ErrorResponse],
)
async def product_detail(
        response: Response,
        pk: int,
        service: Annotated[ProductService, Depends(get_product_service)],
) -> Union[Product, ErrorResponse]:
    """
    Retrieve product.

    Returns:
        Response with product details.
    """
    try:
        product = await service.detail(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return product


@router.get(
    ProductRoutesPrefixes.search,
    status_code=status.HTTP_200_OK,
)
async def search_products(
        keyword: str,
        service: Annotated[ProductService, Depends(get_product_service)],
):
    """
    Search products.

    Returns:
        Response with products.
    """
    response = await service.search(keyword=keyword)
    return response


@router.post(
    ProductRoutesPrefixes.update_index,
    status_code=status.HTTP_200_OK,
)
async def update_product_index(
        background_tasks: BackgroundTasks,
        service: Annotated[ProductService, Depends(get_product_service)],
):
    """
    Update products index.

    Returns:
        None.
    """
    uuid = str(uuid4())
    status_model = TaskStatusModel(uuid=uuid, status=TaskStatus.IN_PROGRESS)
    await status_model.save_to_redis()

    background_tasks.add_task(service.update_search_index, uuid)

    return await TaskStatusModel.get_from_redis(uuid=status_model.uuid)


@router.get("/categories/search")
async def search_categories(keyword: str, service: CategoryService = Depends(get_category_service)):
    """
    Search categories.

    Returns:
        Response with categories.
    """
    return await service.search(keyword=keyword)


@router.post("/categories/update-index")
async def update_category_index(
        background_tasks: BackgroundTasks, service: CategoryService = Depends(get_category_service)):
    """
    Update categories index.

    Returns:
        None.
    """
    uuid = str(uuid4())
    status_model = TaskStatusModel(uuid=uuid, status=TaskStatus.IN_PROGRESS)
    await status_model.save_to_redis()

    background_tasks.add_task(service.update_category_index, uuid)

    return await TaskStatusModel.get_from_redis(uuid=status_model.uuid)
