import random
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi_pagination import LimitOffsetPage, paginate

from api.v1.match.repositories import get_mapped, post_mapped, get_matcheds
from api.v1.match.schemas import ProductDealerKey, ProductDealer
from api.v1.products.depends import product_by_id
from api.v1.products.schemas import Product
from core.db_helper import db_helper
from fastapi import Query

router = APIRouter(prefix="/matching", tags=["Сопоставление"])


@router.get(
    "/{product_id}/",
    summary="Получить сопоставляемые товары заказчика",
    response_model=List[Product],
)
async def get_mapped_products(
    count: int = Query(ge=1, le=25, default=5),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    product: Product = Depends(product_by_id),
):
    print(product)  # будет передаваться в match
    products_id = [random.randint(1, 300) for _ in range(count)]
    return await get_mapped(session=session, products_id=products_id)


@router.post(
    "",
    summary="Сопоставить товары",
    response_model=ProductDealerKey,
)
async def post_mapped_products(
    mapped_in: ProductDealerKey,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await post_mapped(session=session, mapped_in=mapped_in)


@router.get(
    "/all",
    summary="Получить уже сопоставленные товары",
    response_model=LimitOffsetPage[ProductDealer],
)
async def get_matched(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_matcheds(session=session)
    return paginate(value)
