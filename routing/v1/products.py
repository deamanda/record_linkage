from typing import List

from fastapi import APIRouter, Depends
from services.depends import get_product_service

from schemas.products import Product
from services.products import ProductService

router = APIRouter(prefix="/products", tags=["products_v1"])


@router.get(
    "",
    responses={400: {"message": "Bad"}},
    response_model=List[Product],
    description="Получить все продкуты",
)
async def get_all_books(
    product_service: ProductService = Depends(get_product_service),
) -> List[Product]:
    product = product_service.get_product()
    return product
