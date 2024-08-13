from fastapi import APIRouter, Depends, HTTPException
from .services import ProductService, ProductAnalyticsService
from .models.pydantic import ProductModel
from .repository import init_repository

router = APIRouter()

async def get_product_service() -> ProductService:
    repository = await init_repository()
    return ProductService(repository=repository)

async def get_product_analytics_service() -> ProductAnalyticsService:
    repository = await ProductAnalyticsService.init_repository()
    return ProductAnalyticsService(product_analytics_repo=repository)

@router.get("/product_detail/{product_id}", response_model=ProductModel)
async def product_detail(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
    analytics_service: ProductAnalyticsService = Depends(get_product_analytics_service)
):
    await analytics_service.record_product_visit(product_id)

    product = await product_service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product