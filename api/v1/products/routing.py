from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from api.v1.products.depends import product_by_id
from api.v1.products.repositories import get_products, get_product
from api.v1.products.schemas import ProductResponse, Product
from fastapi import File, UploadFile
from core.db_helper import db_helper
from fastapi import Query

from services.products import imports_product

router = APIRouter(prefix="/products", tags=["Товары заказчика"])


@router.post("/import-csv/", summary="Импорт данных заказчика из CSV")
async def imports_product_csv(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await imports_product(file, session)
    return {"message": "CSV data imported successfully"}


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
