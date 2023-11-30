from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from api.v1.match.schemas import ProductDealerKey
from core.db_helper import db_helper
from models import Product, DealerPrice


async def product_dealer_validate(
    mapped_in: ProductDealerKey,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    dealer_price = select(DealerPrice).where(DealerPrice.id == mapped_in.key)
    result = await session.execute(dealer_price)
    if not result.scalar():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dealer price with key {mapped_in.key} not found.",
        )
    product = select(Product).where(Product.id == mapped_in.product_id)
    result_product = await session.execute(product)
    if not result_product.scalar():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with product_id {mapped_in.product_id} not found.",
        )
