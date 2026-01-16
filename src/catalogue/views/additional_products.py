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

from src.catalogue.models.database import AdditionalProduct
from src.catalogue.routes import (
    CatalogueRoutesPrefixes,
    AdditionalProductsRoutesPrefixes,
)
from src.catalogue.services import get_additional_products_service
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse


router = APIRouter(prefix=CatalogueRoutesPrefixes.additional_products)


@router.get(
    AdditionalProductsRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[AdditionalProduct],
)
async def additional_products_list(service: Annotated[get_additional_products_service, Depends()]) -> list[AdditionalProduct]:
    """
    Get list of additional products.

    Returns:
        Response with list of additional products.
    """
    return await service.list()


@router.get(
    AdditionalProductsRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': AdditionalProduct},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[AdditionalProduct, ErrorResponse],
)
async def additional_products_detail(
    response: Response,
    pk: int,
    service: Annotated[get_additional_products_service, Depends()],
) -> Union[Response, ErrorResponse]:
    """
    Retrieve additional product.

    Returns:
        Response with additional product details.
    """
    try:
        response = await service.detail(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response


@router.post(
    AdditionalProductsRoutesPrefixes.root,
    status_code=status.HTTP_201_CREATED,
    response_model=AdditionalProduct,
)
async def additional_products_create(
    additional_product_data: AdditionalProduct,
    service: Annotated[get_additional_products_service, Depends()],
) -> AdditionalProduct:
    """
    Create additional product.

    Returns:
        Response with created additional product.
    """
    return await service.create(additional_product_data)


@router.put(
    AdditionalProductsRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': AdditionalProduct},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[AdditionalProduct, ErrorResponse],
)
async def additional_products_update(
    response: Response,
    pk: int,
    additional_product_data: AdditionalProduct,
    service: Annotated[get_additional_products_service, Depends()],
) -> Union[Response, ErrorResponse]:
    """
    Update additional product.

    Returns:
        Response with updated additional product.
    """
    try:
        response = await service.update(pk=pk, update_data=additional_product_data)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response


@router.delete(
    AdditionalProductsRoutesPrefixes.detail,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def additional_products_delete(
    pk: int,
    service: Annotated[get_additional_products_service, Depends()],
) -> None:
    """
    Delete additional product.

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