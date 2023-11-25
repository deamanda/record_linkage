from typing import List, Dict, Union

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from api.v1.schemas.products import Product
from api.v1.repositories import products
from fastapi import File, UploadFile
from core.db_helper import db_helper
from fastapi import Query

from services.products import imports_product

router = APIRouter(prefix="/products", tags=["products_v1"])


@router.get("", response_model=Dict[str, Union[List[Product], Dict[str, int]]])
async def get_all_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    page: int = Query(ge=0, default=0),
    size: int = Query(ge=1, le=100, default=10),
):
    return await products.get_products(session=session, page=page, size=size)


@router.post("/import-csv/")
async def imports_product_csv(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await imports_product(file, session)
    return {"message": "CSV data imported successfully"}
