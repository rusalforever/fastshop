from typing import (
    Annotated,
    Union,
)

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from src.catalogue.models.pydantic import ProductModel
from src.catalogue.routes import (
    CatalogueRoutesPrefixes,
    ProductRoutesPrefixes,
)
from src.catalogue.services import (
    get_product_service,
)
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse


product_router = APIRouter(prefix=CatalogueRoutesPrefixes.product)


@product_router.get(
    ProductRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[ProductModel],
)
# async def product_list(product_service: Annotated[get_product_service, Depends()]) -> list[ProductModel]:
async def product_list(product_service=Depends(get_product_service)) -> list[ProductModel]:

    """
    Get list of products.

    Returns:
        Response with list of products.
    """
    return await product_service.list()


@product_router.get(
    ProductRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': ProductModel},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[ProductModel, ErrorResponse],
)
async def product_detail(
    response: Response,
    pk: int,
    service: Annotated[get_product_service, Depends()],
) -> Union[Response, ErrorResponse]:
    """
    Retrieve product.

    Returns:
        Response with product details.
    """
    try:
        response = await service.detail(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response
