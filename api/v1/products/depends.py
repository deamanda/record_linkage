from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path
from typing import Annotated
from api.v1.products.repositories import get_product

from core.db_helper import db_helper


from models import Product


async def product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    """Checking product availability by ID"""
    product = await get_product(session=session, product_id=product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Товар с id = {product_id} не найден.",
        )
    return product
