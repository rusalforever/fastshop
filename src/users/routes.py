from fastapi import APIRouter, BackgroundTasks
from elasticsearch_dsl import Search, Index
from .services import CategoryService 
from src.common.databases.redis import get_redis_client
from src.common.routes import BaseCrudPrefixes

class CategoryIndex:
    _index = Index('category_index')

router = APIRouter()

redis_client = get_redis_client()

class CatalogueRoutesPrefixes:
    product: str = '/product'

class ProductRoutesPrefixes(BaseCrudPrefixes):
    search: str = '/search'
    update_index: str = '/update-index'

@router.get(CatalogueRoutesPrefixes.product + ProductRoutesPrefixes.search)
async def search_categories(query: str):
    """
    Search for categories based on a query string.
    
    Args:
        query: The query string to search for in category titles and descriptions.
        
    Returns:
        A dictionary containing the search results.
    """
    search = Search(index=CategoryIndex._index._name).query("multi_match", query=query, fields=["title", "description"])
    response = await search.execute()
    return response.to_dict()

@router.post(CatalogueRoutesPrefixes.product + ProductRoutesPrefixes.update_index)
async def update_index(background_tasks: BackgroundTasks):
    """
    Trigger a background task to update the category index.
    
    Args:
        background_tasks: FastAPI BackgroundTasks instance to manage background tasks.
        
    Returns:
        A message indicating that the index update has started.
    """
    category_service = CategoryService(redis_client=redis_client)
    background_tasks.add_task(category_service.update_category_index)
    return {"message": "Index update started"}

@router.get("/index-status")
async def get_index_status():
    """
    Get the current status of the category index update.
    
    Returns:
        A dictionary containing the index status.
    """
    category_service = CategoryService(redis_client=redis_client)
    return {"status": category_service.get_index_status()}
