from datetime import datetime
from typing import Sequence

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.analytics.depends import count_match
from models import Dealer
from models.dealers import Dealer


async def get_dealer(session: AsyncSession, dealerprice) -> Dealer | None:
    return await session.get(Dealer, dealerprice.dealer_id)


async def get_compared(
    start_date: datetime,
    end_date: datetime,
    session: AsyncSession,
) -> dict:
    matched = await count_match(
        start_date=start_date,
        end_date=end_date,
        session=session,
        match_status="matched",
    )
    not_matched = await count_match(
        start_date=start_date,
        end_date=end_date,
        session=session,
        match_status="not matched",
    )
    deferred = await count_match(
        start_date=start_date,
        end_date=end_date,
        session=session,
        match_status="deferred",
    )
    total_matching = matched + not_matched
    accuracy = matched / total_matching if total_matching > 0 else 0.0
    await session.close()
    return {
        "matched": matched,
        "not_matched": not_matched,
        "deferred": deferred,
        "total_matching": total_matching,
        "accuracy": accuracy,
    }


async def get_dealers(session: AsyncSession) -> Sequence[Dealer]:
    stmt = select(Dealer).order_by(Dealer.id)
    result = await session.execute(stmt)
    all_dealers = result.scalars().all()
    await session.close()
    return all_dealers
