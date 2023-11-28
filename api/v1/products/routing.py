from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from api.v1.products.depends import product_by_id
from api.v1.products.repositories import get_products
from api.v1.products.schemas import ProductResponse, Product
from core.db_helper import db_helper
from fastapi import Query

router = APIRouter(prefix="/products", tags=["Товары заказчика"])


@router.get(
    "/{product_id}/",
    response_model=Product,
    summary="Получить товар заказчика",
)
async def get_product(product: Product = Depends(product_by_id)):
    return product


@router.get(
    "",
    response_model=ProductResponse,
    summary="Получить все товары заказчика",
)
async def get_all_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=10),
):
    return await get_products(session=session, page=page, size=size)
