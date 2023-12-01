from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, UploadFile, File, Query

from api.v1.products.depends import product_by_id
from api.v1.products.repositories import get_products
from api.v1.products.schemas import Product
from core.db_helper import db_helper
from fastapi_pagination import LimitOffsetPage, paginate

from services.import_csv.products import imports_product

router = APIRouter(prefix="/products", tags=["Товары заказчика"])


@router.get(
    "/{product_id}/",
    response_model=Product,
    summary="Получить товар заказчика",
)
async def get_product(product: Product = Depends(product_by_id)):
    return product


@router.post("/import-csv/", summary="Импорт данных заказчика из CSV")
async def imports_product_csv(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await imports_product(file, session)
    return {"message": "CSV data imported successfully"}


@router.get(
    "",
    response_model=LimitOffsetPage[Product],
    summary="Получить все товары заказчика",
)
async def get_all_products(
    search_query: str = Query(default=None, description="Search"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_products(session=session, search_query=search_query)
    return paginate(value)
