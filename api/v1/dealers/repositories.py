from typing import Sequence

from sqlalchemy import or_, desc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import DealerPrice, Dealer, ProductDealer
from models.dealers import DealerPrice, Dealer
from services.choices import SortedField


async def get_dealer(session: AsyncSession, dealerprice) -> Dealer | None:
    """Receiving dealer data"""
    return await session.get(Dealer, dealerprice.dealer_id)


async def get_dealerprices(
    session: AsyncSession,
    sort_by: SortedField | None,
    status: str | None,
    search_query: str,
) -> Sequence[DealerPrice]:
    """Receiving dealer's goods"""
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
            or_(
                (ProductDealer.status == status)
                if status in ["not matched", "matched", "deferred"]
                else (
                    ProductDealer.id.is_(None)
                    if status == "not processed"
                    else True
                ),
            ),
            DealerPrice.product_name.ilike(f"%{search_query}%")
            if search_query
            else True,
        )
    )

    if sort_by == "descending price":
        query = query.order_by(desc(DealerPrice.price))
    elif sort_by == "ascending price":
        query = query.order_by(DealerPrice.price)
    elif sort_by == "ascending time":
        query = query.order_by(DealerPrice.date)
    elif sort_by == "descending time":
        query = query.order_by(desc(DealerPrice.date))
    else:
        query = query.order_by(DealerPrice.id)

    result = await session.execute(query)
    all_dealerprices = result.scalars().all()
    await session.close()
    return all_dealerprices


async def get_dealerprice(
    session: AsyncSession, dealerprice_id: int
) -> DealerPrice | None:
    """Receiving dealer's goods by ID"""
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
    """Getting a list of dealers"""
    stmt = select(Dealer).order_by(Dealer.id)
    result = await session.execute(stmt)
    all_dealers = result.scalars().all()
    await session.close()
    return all_dealers
