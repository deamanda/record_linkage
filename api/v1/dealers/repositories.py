from typing import Sequence

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import DealerPrice, Dealer
from models.dealers import DealerPrice, Dealer


async def get_dealerprices(session: AsyncSession) -> Sequence[DealerPrice]:
    stmt = select(DealerPrice).order_by(DealerPrice.id)
    result = await session.execute(stmt)
    all_dealerprices = result.scalars().all()
    return all_dealerprices


async def get_dealerprice(
    session: AsyncSession, dealerprice_id: int
) -> DealerPrice | None:
    return await session.get(DealerPrice, dealerprice_id)


async def get_dealer(session: AsyncSession) -> Sequence[Dealer]:
    stmt = select(Dealer).order_by(Dealer.id)
    result = await session.execute(stmt)
    all_dealers = result.scalars().all()
    return all_dealers
