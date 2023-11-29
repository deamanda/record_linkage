from fastapi import Depends, HTTPException, status

from core.db_helper import db_helper
from sqlalchemy import and_, update, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.match.schemas import ProductDealerKey
from models import DealerPrice
from models.products import Product
from models.product_dealer import ProductDealer


async def product_dealer_validate(
    mapped_in: ProductDealerKey,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    dealer_price = select(DealerPrice).where(DealerPrice.id == mapped_in.key)
    result = await session.execute(dealer_price)
    if not result.scalar():
        await session.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dealer price with key={mapped_in.key} not found.",
        )
    product = select(Product).where(Product.id == mapped_in.product_id)
    result_product = await session.execute(product)
    if not result_product.scalar():
        await session.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with product_id={mapped_in.product_id} not found.",
        )


async def matching(
    match_status_1: bool,
    match_status_2: bool,
    mapped_in: ProductDealerKey,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    dealer_id = await session.get(DealerPrice, mapped_in.key)
    dealer_price = select(ProductDealer).where(
        and_(
            ProductDealer.key == mapped_in.key,
            ProductDealer.product_id == mapped_in.product_id,
            ProductDealer.dealer_id == dealer_id.dealer_id,
        )
    )
    result = await session.execute(dealer_price)
    dealer_price_result = result.scalar()
    if dealer_price_result:
        if dealer_price_result.status is match_status_2:
            new_dealer_price = (
                update(ProductDealer)
                .where(
                    and_(
                        ProductDealer.key == mapped_in.key,
                        ProductDealer.product_id == mapped_in.product_id,
                        ProductDealer.dealer_id == dealer_id.dealer_id,
                    )
                )
                .values(status=match_status_1, created_at=func.now())
            )
            await session.execute(new_dealer_price)
        elif dealer_price_result.status is match_status_1:
            await session.close()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Item has already been matched!",
            )
    else:
        await product_dealer_validate(session=session, mapped_in=mapped_in)
        mapped = ProductDealer(**mapped_in.model_dump(), status=match_status_1)
        session.add(mapped)

    await session.commit()
