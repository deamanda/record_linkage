from typing import Sequence

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.dealers import DealerPrice, Dealer
from services.pagination import pagination


async def get_dealerprices(
    session: AsyncSession, page: int, size: int
) -> dict[str, Sequence[DealerPrice] | dict[str, int]]:
    stmt = select(DealerPrice).order_by(DealerPrice.id)
    result = await session.execute(stmt)
    all_dealerprices = result.scalars().all()
    return pagination(page, size, all_dealerprices)


async def get_dealerprice(
    session: AsyncSession, dealerprice_id: int
) -> DealerPrice | None:
    return await session.get(DealerPrice, dealerprice_id)


async def get_dealer(
    session: AsyncSession, page: int, size: int
) -> dict[str, Sequence[Dealer] | dict[str, int]]:
    stmt = select(Dealer).order_by(Dealer.id)
    result = await session.execute(stmt)
    all_dealers = result.scalars().all()
    return pagination(page, size, all_dealers)
