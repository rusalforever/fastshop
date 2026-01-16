from typing import (
    Annotated,
    Union,
)

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from src.catalogue.models.database import RecommendedProduct
from src.catalogue.routes import (
    CatalogueRoutesPrefixes,
    RecommendedProductsRoutesPrefixes,
)
from src.catalogue.services import get_recommended_products_service
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse


router = APIRouter(prefix=CatalogueRoutesPrefixes.recommended_products)


@router.get(
    RecommendedProductsRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[RecommendedProduct],
)
async def recommended_products_list(service: Annotated[get_recommended_products_service, Depends()]) -> list[RecommendedProduct]:
    """
    Get list of recommended products.

    Returns:
        Response with list of recommended products.
    """
    return await service.list()


@router.get(
    RecommendedProductsRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': RecommendedProduct},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[RecommendedProduct, ErrorResponse],
)
async def recommended_products_detail(
    response: Response,
    pk: int,
    service: Annotated[get_recommended_products_service, Depends()],
) -> Union[Response, ErrorResponse]:
    """
    Retrieve recommended product.

    Returns:
        Response with recommended product details.
    """
    try:
        response = await service.detail(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response


@router.post(
    RecommendedProductsRoutesPrefixes.root,
    status_code=status.HTTP_201_CREATED,
    response_model=RecommendedProduct,
)
async def recommended_products_create(
    recommended_product_data: RecommendedProduct,
    service: Annotated[get_recommended_products_service, Depends()],
) -> RecommendedProduct:
    """
    Create recommended product.

    Returns:
        Response with created recommended product.
    """
    return await service.create(recommended_product_data)


@router.put(
    RecommendedProductsRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': RecommendedProduct},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[RecommendedProduct, ErrorResponse],
)
async def recommended_products_update(
    response: Response,
    pk: int,
    recommended_product_data: RecommendedProduct,
    service: Annotated[get_recommended_products_service, Depends()],
) -> Union[Response, ErrorResponse]:
    """
    Update recommended product.

    Returns:
        Response with updated recommended product.
    """
    try:
        response = await service.update(pk=pk, update_data=recommended_product_data)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response


@router.delete(
    RecommendedProductsRoutesPrefixes.detail,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def recommended_products_delete(
    pk: int,
    service: Annotated[get_recommended_products_service, Depends()],
) -> None:
    """
    Delete recommended product.

    Returns:
        Response confirming deletion.
    """
    try:
        await service.delete(pk=pk)
    except ObjectDoesNotExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message
        )