from typing import List, Dict, Union

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from api.v1.products.repositories import get_products
from api.v1.products.schemas import Product
from core.db_helper import db_helper
from fastapi import Query


router = APIRouter(prefix="/dealers", tags=["Товары дилера"])


@router.get(
    "",
    response_model=Dict[str, Union[List[Product], Dict[str, int]]],
    summary="Получить товары дилеров",
)
async def get_all_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    page: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=100, default=10),
):
    return await get_products(session=session, page=page, size=size)
