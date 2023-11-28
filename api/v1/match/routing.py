import random
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Body

from api.v1.match.repositories import get_mapped
from api.v1.products.depends import product_by_id
from api.v1.products.schemas import Product
from fastapi import File, UploadFile
from core.db_helper import db_helper
from fastapi import Query

from services.match import match

router = APIRouter(prefix="/match", tags=["Товары заказчика"])


@router.post("/import-csv/", summary="Импорт данных заказчика из CSV")
async def imports_product_csv_s(
    file: UploadFile = File(...),
    name: List[str] = Body(),
    count: int = Body(ge=1, le=100, default=5),
):
    value = await match(name, count, file)
    return value


@router.get(
    "/{product_id}/",
    summary="Получить сопоставленные товары заказчика",
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
