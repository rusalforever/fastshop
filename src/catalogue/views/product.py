from typing import (
    Annotated,
    Union,
    List,
)

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    HTTPException,
)

from src.catalogue.models.pydantic import ProductModel
from src.catalogue.routes import (
    CatalogueRoutesPrefixes,
    ProductRoutesPrefixes,
)
from src.catalogue.services import get_product_service
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse
from src.catalogue.routes import CatalogueRoutesPrefixes, ProductRoutesPrefixes
from src.routes import get_product_service
from ..services import ProductService



router = APIRouter(prefix=CatalogueRoutesPrefixes.product)


@router.get(
    ProductRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=List[ProductModel],
)
async def product_list(
    product_service: Annotated[get_product_service, Depends()]
) -> List[ProductModel]:
    return await product_service.list()


@router.get(
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
) -> Union[ProductModel, ErrorResponse]:
    
    try:
        return await service.detail(pk=pk)
    except ObjectDoesNotExistException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
