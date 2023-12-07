from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.analytics.depends import count_match, get_position_statistics
from models import User


async def get_compared(
    start_date: datetime,
    end_date: datetime,
    session: AsyncSession,
    user: User = None,
    dealer_id: int = None,
    user_id: int = None,
) -> dict:
    """Getting and calculating statistics on comparisons"""
    user_local = await session.merge(user) if user else None
    matched = await count_match(
        start_date=start_date,
        end_date=end_date,
        session=session,
        match_status="matched",
        user=user_local,
        dealer_id=dealer_id,
        user_id=user_id,
    )
    not_matched = await count_match(
        start_date=start_date,
        end_date=end_date,
        session=session,
        match_status="not matched",
        user=user_local,
        dealer_id=dealer_id,
        user_id=user_id,
    )
    deferred = await count_match(
        start_date=start_date,
        end_date=end_date,
        session=session,
        match_status="deferred",
        user=user_local,
        dealer_id=dealer_id,
        user_id=user_id,
    )

    total_matching = matched + not_matched
    accuracy = matched / total_matching if total_matching > 0 else 0.0

    position = await get_position_statistics(
        session=session,
        start_date=start_date,
        end_date=end_date,
        user=user_local,
        dealer_id=dealer_id,
        user_id=user_id,
    )
    await session.close()
    return {
        "matched": matched,
        "not_matched": not_matched,
        "deferred": deferred,
        "total_matching": total_matching,
        "accuracy": accuracy,
        "position": position,
    }
