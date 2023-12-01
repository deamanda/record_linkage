from typing import Sequence

from sqlalchemy import or_
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
    price: bool,
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
        .order_by()
    )

    result = await session.execute(query)
    all_dealerprices = result.scalars().all()
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
    return dealerprice


async def get_dealers(session: AsyncSession) -> Sequence[Dealer]:
    stmt = select(Dealer).order_by(Dealer.id)
    result = await session.execute(stmt)
    all_dealers = result.scalars().all()
    return all_dealers
