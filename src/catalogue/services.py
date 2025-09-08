from typing import Optional
from fastapi import Depends

from src.catalogue.models.database import (
    Product,
    AdditionalProducts,
    RecommendedProducts,
)
from src.catalogue.repository import (
    ProductRepository,
    get_product_repository,
    AdditionalProductsRepository,
    get_additional_products_repository,
    RecommendedProductsRepository,
    get_recommended_products_repository,
)
from src.common.service import BaseService


class ProductService(BaseService[Product]):
    def __init__(
        self, 
        repository: ProductRepository,
        additional_products_service: Optional["AdditionalProductsService"] = None,
        recommended_products_service: Optional["RecommendedProductsService"] = None
    ):
        super().__init__(repository)
        self._additional_products_service = additional_products_service
        self._recommended_products_service = recommended_products_service
    
    async def get_product_with_related(self, product_id: int) -> dict:
        """Отримати товар разом із додатковими та рекомендованими товарами."""
        product = await self.repository.get(pk=product_id)
        if not product:
            return None
            
        result = {
            "product": product,
            "additional_products": [],
            "recommended_products": []
        }
        
        if self._additional_products_service:
            result["additional_products"] = await self._additional_products_service.get_additional_products_for_product(product_id)
            
        if self._recommended_products_service:
            result["recommended_products"] = await self._recommended_products_service.get_recommended_products_for_product(product_id)
            
        return result


class AdditionalProductsService(BaseService[AdditionalProducts]):
    def __init__(self, repository: AdditionalProductsRepository):
        super().__init__(repository)
    
    async def get_additional_products_for_product(self, product_id: int) -> list[AdditionalProducts]:
        """Get additional products for product by ID."""
        return await self.repository.filter(primary_id=product_id)
    
    async def get_additional_product_by_id(self, additional_product_id: int) -> AdditionalProducts | None:
        """Get additional product by ID."""
        return await self.repository.get(pk=additional_product_id)
    
    async def add_additional_product(self, primary_id: int, additional_id: int) -> AdditionalProducts:
        """Add additional product to main product by ID."""

        existing = await self.repository.filter(primary_id=primary_id, additional_id=additional_id)
        if existing:
            raise ValueError(f"Additional product {additional_id} already related to {primary_id}")
        

        if primary_id == additional_id:
            raise ValueError("Can't add additional product to the same product.")
            
        additional_product = AdditionalProducts(primary_id=primary_id, additional_id=additional_id)
        return await self.repository.create(additional_product)
    
    async def update_additional_product(self, additional_product_id: int, primary_id: int, additional_id: int) -> AdditionalProducts:
        """Update additional product by ID. It's possible to change primary_id and additional_id at the same time."""
        if primary_id == additional_id:
            raise ValueError("Product can't be related to itself.")

        existing = await self.repository.filter(primary_id=primary_id, additional_id=additional_id)
        if existing and any(item.id != additional_product_id for item in existing):
            raise ValueError(f"Addtiional product {additional_id} already related to {primary_id}")
            
        update_data = AdditionalProducts(primary_id=primary_id, additional_id=additional_id)
        return await self.repository.update(pk=additional_product_id, update_data=update_data)
    
    async def remove_additional_product(self, additional_product_id: int) -> None:
        """Remove additional product by ID."""
        await self.repository.delete(pk=additional_product_id)
    
    async def remove_additional_product_by_ids(self, primary_id: int, additional_id: int) -> bool:
        """Remove additional product by ID. It's possible to remove multiple additional products for one product."""
        existing = await self.repository.filter(primary_id=primary_id, additional_id=additional_id)
        if not existing:
            return False
            
        for item in existing:
            await self.repository.delete(pk=item.id)
        return True
    
    async def count_additional_products_for_product(self, product_id: int) -> int:
        """Calculate count of additional products for product by ID."""
        additional_products = await self.repository.filter(primary_id=product_id)
        return len(additional_products)


class RecommendedProductsService(BaseService[RecommendedProducts]):
    def __init__(self, repository: RecommendedProductsRepository):
        super().__init__(repository)
    
    async def get_recommended_products_for_product(self, product_id: int) -> list[RecommendedProducts]:
        """Get recommended products for product by ID."""
        return await self.repository.filter(primary_id=product_id)
    
    async def get_recommended_product_by_id(self, recommended_product_id: int) -> RecommendedProducts | None:
        """Get recommended product by ID."""
        return await self.repository.get(pk=recommended_product_id)
    
    async def add_recommended_product(self, primary_id: int, recommended_id: int) -> RecommendedProducts:
        """Add recommended product to main product by ID."""
        existing = await self.repository.filter(primary_id=primary_id, recommended_id=recommended_id)
        if existing:
            raise ValueError(f"Recommended {recommended_id} already related to {primary_id}")
        

        if primary_id == recommended_id:
            raise ValueError("Product can't be recommended to itself.")
            
        recommended_product = RecommendedProducts(primary_id=primary_id, recommended_id=recommended_id)
        return await self.repository.create(recommended_product)
    
    async def update_recommended_product(self, recommended_product_id: int, primary_id: int, recommended_id: int) -> RecommendedProducts:
        if primary_id == recommended_id:
            raise ValueError("Product can't be recommended to itself.")
            

        existing = await self.repository.filter(primary_id=primary_id, recommended_id=recommended_id)
        if existing and any(item.id != recommended_product_id for item in existing):
            raise ValueError(f"Recommended product {recommended_id} already related {primary_id}")
            
        update_data = RecommendedProducts(primary_id=primary_id, recommended_id=recommended_id)
        return await self.repository.update(pk=recommended_product_id, update_data=update_data)
    
    async def remove_recommended_product(self, recommended_product_id: int) -> None:
        """Remove recommended product by ID. It's possible to remove multiple recommended products for one product by ID."""
        await self.repository.delete(pk=recommended_product_id)
    
    async def remove_recommended_product_by_ids(self, primary_id: int, recommended_id: int) -> bool:
        """Remove recommended product relationship by ID. It's possible to remove multiple recommended products for one product by ID."""
        existing = await self.repository.filter(primary_id=primary_id, recommended_id=recommended_id)
        if not existing:
            return False
            
        for item in existing:
            await self.repository.delete(pk=item.id)
        return True
    
    async def count_recommended_products_for_product(self, product_id: int) -> int:
        """Calculate count of recommended products for product by ID."""
        recommended_products = await self.repository.filter(primary_id=product_id)
        return len(recommended_products)


def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)


def get_additional_products_service(
    repo: AdditionalProductsRepository = Depends(get_additional_products_repository)
) -> AdditionalProductsService:
    return AdditionalProductsService(repository=repo)


def get_recommended_products_service(
    repo: RecommendedProductsRepository = Depends(get_recommended_products_repository)
) -> RecommendedProductsService:
    return RecommendedProductsService(repository=repo)
