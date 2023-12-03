from typing import Sequence

from sqlalchemy import or_, desc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import DealerPrice, Dealer, ProductDealer
from models.dealers import DealerPrice, Dealer


async def get_dealer(session: AsyncSession, dealerprice) -> Dealer | None:
    return await session.get(Dealer, dealerprice.dealer_id)


async def get_dealerprices(
    session: AsyncSession,
    sort_by_date: bool,
    status: str,
    search_query: str,
    sort_by_price: bool,
) -> Sequence[DealerPrice]:
    query = (
        select(DealerPrice)
        .options(
            joinedload(DealerPrice.dealer),
            joinedload(DealerPrice.productdealer).joinedload(
                ProductDealer.product
            ),
        )
        .outerjoin(ProductDealer, ProductDealer.key == DealerPrice.id)
        .filter(
            or_(ProductDealer.status == status, status is None),
            DealerPrice.product_name.ilike(f"%{search_query}%")
            if search_query
            else True,
        )
    )
    if sort_by_price is True:
        query = query.order_by(desc(DealerPrice.price))
    elif sort_by_price is False:
        query = query.order_by(DealerPrice.price)
    elif sort_by_date is False:
        query = query.order_by(DealerPrice.date)
    else:
        query = query.order_by(desc(DealerPrice.date))

    result = await session.execute(query)
    all_dealerprices = result.scalars().all()
    await session.close()
    return all_dealerprices


async def get_dealerprice(
    session: AsyncSession, dealerprice_id: int
) -> DealerPrice | None:
    stmt = (
        select(DealerPrice)
        .where(DealerPrice.id == dealerprice_id)
        .options(
            joinedload(DealerPrice.dealer),
            joinedload(DealerPrice.productdealer).joinedload(
                ProductDealer.product
            ),
        )
    )
    result = await session.execute(stmt)
    dealerprice = result.scalar()
    await session.close()
    return dealerprice


async def get_dealers(session: AsyncSession) -> Sequence[Dealer]:
    stmt = select(Dealer).order_by(Dealer.id)
    result = await session.execute(stmt)
    all_dealers = result.scalars().all()
    await session.close()
    return all_dealers
