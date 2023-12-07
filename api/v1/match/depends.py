from fastapi import Depends, HTTPException, status

from core.db_helper import db_helper
from sqlalchemy import and_, update, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import numpy as np
from api.v1.match.schemas import ProductDealerKey, ProductDealerKeyNone
from models import DealerPrice, User, ModelVector, Product
from models.match import ProductsMapped
from models.product_dealer import ProductDealer
from services.DS_match.match import norm_name, create_embeddings, match
from services.validators import validate_availability_check


async def matching(
    match_status: str,
    mapped_in: ProductDealerKey,
    user: User,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Matching function. If there is no matching,
    then creates it, if there is, then changes it to “matched”"""
    user_local = await session.merge(user)
    dealer_id = await session.get(DealerPrice, mapped_in.key)
    dealer_price = select(ProductDealer).where(
        and_(
            ProductDealer.key == mapped_in.key,
            ProductDealer.product_id == mapped_in.product_id,
            ProductDealer.dealer_id == dealer_id.dealer_id,
            ProductDealer.status == match_status,
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
        pos = select(ProductsMapped).where(
            and_(
                ProductsMapped.dealerprice_id == mapped_in.key,
                ProductsMapped.product_id == mapped_in.product_id,
            )
        )
        position = await session.execute(pos)
        result_position = position.scalar()
        if not result_position:
            await session.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not yet!",
            )
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
                    position=result_position.position,
                )
            )
            await session.execute(new_dealer_price)
        else:
            await validate_availability_check(
                Product, mapped_in.product_id, session, "Product"
            )
            await validate_availability_check(
                DealerPrice, mapped_in.key, session, "Dealer Price"
            )

            mapped = ProductDealer(
                **mapped_in.model_dump(),
                status=match_status,
                user=user_local,
                position=result_position.position,
            )
            session.add(mapped)
    await session.commit()
    await session.close()


async def not_matching(
    match_status: str,
    mapped_in: ProductDealerKeyNone,
    user: User,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Matching function. If there is no matching,
    then it creates it, if there is, then it changes to “not matched”"""
    user_local = await session.merge(user)
    dealer_id = await session.get(DealerPrice, mapped_in.key)
    dealer_price = select(ProductDealer).where(
        and_(
            ProductDealer.key == mapped_in.key,
            ProductDealer.product_id == None,
            ProductDealer.dealer_id == dealer_id.dealer_id,
            ProductDealer.status == match_status,
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
                    position=None,
                )
            )
            await session.execute(new_dealer_price)
        else:
            await validate_availability_check(
                DealerPrice, mapped_in.key, session, "Dealer Price"
            )
            mapped = ProductDealer(
                **mapped_in.model_dump(),
                status=match_status,
                user=user_local,
                position=None,
            )
            session.add(mapped)
    await session.commit()
    await session.close()


async def matching_later(
    match_status: str,
    mapped_in: ProductDealerKeyNone,
    user: User,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Matching function. If there is no matching,
    then it creates it, if there is, then it changes to “deferred”"""
    user_local = await session.merge(user)
    dealer_id = await session.get(DealerPrice, mapped_in.key)
    dealer_price = select(ProductDealer).where(
        and_(
            ProductDealer.key == mapped_in.key,
            ProductDealer.product_id == None,
            ProductDealer.dealer_id == dealer_id.dealer_id,
            ProductDealer.status == match_status,
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
                    status=match_status,
                    created_at=func.now(),
                    product_id=None,
                    position=None,
                )
            )
            await session.execute(new_dealer_price)
        else:
            await validate_availability_check(
                DealerPrice, mapped_in.key, session, "Dealer Price"
            )
            mapped = ProductDealer(
                **mapped_in.model_dump(),
                status=match_status,
                user=user_local,
                position=None,
            )
            session.add(mapped)
    await session.commit()
    await session.close()


async def get_matched(
    session: AsyncSession, dealerprice_id: int, count: int
) -> list:
    """Getting a list of comparable products (ML)"""
    await validate_availability_check(
        DealerPrice, dealerprice_id, session, "Dealer Price"
    )
    result = await session.execute(
        select(ModelVector.product_key, ModelVector.size, ModelVector.value)
    )
    valuse = [[row[0], row[1], list(row[2])] for row in result]
    stmt = select(DealerPrice).where(DealerPrice.id == dealerprice_id)
    result = await session.execute(stmt)
    dealerprice = result.scalar()
    name = norm_name(dealerprice.product_name)
    market_name = [create_embeddings(name[0]), name[1]]
    valuse = np.array(valuse, dtype=object)
    await session.close()
    products = await match(valuse, market_name, count)
    return products[0]
