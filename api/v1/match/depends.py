from fastapi import Depends, HTTPException, status

from core.db_helper import db_helper
from sqlalchemy import and_, update, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.match.schemas import ProductDealerKey, ProductDealerKeyNone
from models import DealerPrice
from models.products import Product
from models.product_dealer import ProductDealer


async def product_validate(
    mapped_in,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    product = select(Product).where(Product.id == mapped_in.product_id)
    result_product = await session.execute(product)
    if not result_product.scalar():
        await session.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with product_id={mapped_in.product_id} not found.",
        )


async def dealer_price_validate(
    mapped_in,
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


async def pre_dealer_price_validate(
    mapped_in,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    dealer_price = select(ProductDealer).where(
        ProductDealer.key == mapped_in.key
    )
    result = await session.execute(dealer_price)
    if result.scalar():
        await session.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item has already been matched!",
        )


async def matching(
    match_status: bool,
    mapped_in: ProductDealerKey,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    dealer_id = await session.get(DealerPrice, mapped_in.key)
    dealer_price = select(ProductDealer).where(
        and_(
            ProductDealer.key == mapped_in.key,
            ProductDealer.product_id == mapped_in.product_id,
            ProductDealer.dealer_id == dealer_id.dealer_id,
            ProductDealer.status == True,
        )
    )
    result = await session.execute(dealer_price)
    dealer_price_result = result.scalar()
    if dealer_price_result:
        await session.close()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Item has already been matched!",
        )
    else:
        dealer_price_another = select(ProductDealer).where(
            and_(
                ProductDealer.key == mapped_in.key,
            )
        )
        result = await session.execute(dealer_price_another)
        dealer_price_result_another = result.scalar()
        if dealer_price_result_another:
            new_dealer_price = (
                update(ProductDealer)
                .where(
                    ProductDealer.id == dealer_price_result_another.id,
                )
                .values(
                    status=match_status,
                    created_at=func.now(),
                    product_id=mapped_in.product_id,
                )
            )
            await session.execute(new_dealer_price)
        else:
            await product_validate(mapped_in=mapped_in, session=session)
            await dealer_price_validate(mapped_in=mapped_in, session=session)
            mapped = ProductDealer(
                **mapped_in.model_dump(), status=match_status
            )
            session.add(mapped)
    await session.commit()
    await session.close()


async def not_matching(
    match_status: bool,
    mapped_in: ProductDealerKeyNone,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    dealer_id = await session.get(DealerPrice, mapped_in.key)
    dealer_price = select(ProductDealer).where(
        and_(
            ProductDealer.key == mapped_in.key,
            ProductDealer.product_id == None,
            ProductDealer.dealer_id == dealer_id.dealer_id,
            ProductDealer.status == False,
        )
    )
    result = await session.execute(dealer_price)
    dealer_price_result = result.first()
    if dealer_price_result:
        await session.close()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Item has already been matched!",
        )
    else:
        dealer_price_another = select(ProductDealer).where(
            and_(
                ProductDealer.key == mapped_in.key,
            )
        )
        result = await session.execute(dealer_price_another)
        dealer_price_result_another = result.scalar()
        if dealer_price_result_another:
            new_dealer_price = (
                update(ProductDealer)
                .where(
                    ProductDealer.id == dealer_price_result_another.id,
                )
                .values(
                    status=match_status,
                    created_at=func.now(),
                    product_id=None,
                )
            )
            await session.execute(new_dealer_price)
        else:
            await dealer_price_validate(mapped_in=mapped_in, session=session)
            mapped = ProductDealer(
                **mapped_in.model_dump(), status=match_status
            )
            session.add(mapped)
    await session.commit()
    await session.close()


async def matching_later(
    match_status: None,
    mapped_in: ProductDealerKeyNone,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    dealer_id = await session.get(DealerPrice, mapped_in.key)
    dealer_price = select(ProductDealer).where(
        and_(
            ProductDealer.key == mapped_in.key,
            ProductDealer.product_id == None,
            ProductDealer.dealer_id == dealer_id.dealer_id,
            ProductDealer.status == None,
        )
    )
    result = await session.execute(dealer_price)
    dealer_price_result = result.scalar()
    if dealer_price_result:
        await session.close()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Item has already been skipped!",
        )
    else:
        dealer_price_another = select(ProductDealer).where(
            and_(
                ProductDealer.key == mapped_in.key,
            )
        )
        result = await session.execute(dealer_price_another)
        dealer_price_result_another = result.scalar()
        if dealer_price_result_another:
            new_dealer_price = (
                update(ProductDealer)
                .where(
                    ProductDealer.id == dealer_price_result_another.id,
                )
                .values(
                    status=None,
                    created_at=func.now(),
                    product_id=None,
                )
            )
            await session.execute(new_dealer_price)
        else:
            await dealer_price_validate(mapped_in=mapped_in, session=session)
            mapped = ProductDealer(
                **mapped_in.model_dump(), status=match_status
            )
            session.add(mapped)
    await session.commit()
    await session.close()
