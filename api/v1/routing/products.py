from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends


from api.v1.schemas.products import Product
from api.v1.repositories import products
from core.db_helper import db_helper

router = APIRouter(prefix="/products", tags=["products_v1"])


@router.get("", response_model=List[Product])
async def get_all_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await products.get_products(session=session)
