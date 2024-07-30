from typing import Annotated, Optional

from fastapi import (
    APIRouter,
    Request,
    Query
)
from fastapi import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.catalogue.models.pydantic import ProductCreate
from src.catalogue.services import get_product_service
from src.ui.routes import UIRoutesPrefixes

router = APIRouter(prefix='')

templates = Jinja2Templates(directory="src/templates")


@router.get(
    UIRoutesPrefixes.filter,
    response_class=HTMLResponse
)
async def filter_products(
        request: Request,
        product_service:
        Annotated[get_product_service, Depends()],
        q: Optional[str] = Query(None)
):
    if q:
        items = await product_service.filter(query=q)
    else:
        items = await product_service.list()
    return templates.TemplateResponse(
        "list.html",
        {"request": request, "items": items, "query": q}
    )


@router.post(
    UIRoutesPrefixes.root,
    response_class=HTMLResponse
)
async def create_product(
        request: Request,
        product_service: Annotated[get_product_service, Depends()],
        product: ProductCreate
):
    await product_service.create(instance_data=product)
    items = await product_service.list()
    return templates.TemplateResponse("list.html", {"request": request, "items": items})


@router.get(
    UIRoutesPrefixes.root,
    response_class=HTMLResponse
)
async def get_products(
        request: Request,
        product_service:
        Annotated[get_product_service, Depends()],
):
    items = await product_service.list()
    return templates.TemplateResponse(
        "products.html",
        {"request": request, "items": items}
    )


@router.delete(
    '/{pk}',
    response_class=HTMLResponse
)
async def delete_product(pk, request: Request, product_service: Annotated[get_product_service, Depends()]):
    await product_service.delete(pk=int(pk))
    items = await product_service.list()
    return templates.TemplateResponse("list.html", {"request": request, "items": items})


@router.get(
    '/{pk}',
    response_class=HTMLResponse
)
async def delete_product(pk, request: Request, product_service: Annotated[get_product_service, Depends()]):
    item = await product_service.detail(pk=int(pk))
    return templates.TemplateResponse("detail.html", {"request": request, "item": item})
