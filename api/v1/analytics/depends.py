from datetime import datetime

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession


from models import ProductDealer


async def count_match(
    match_status: str,
    start_date: datetime,
    end_date: datetime,
    session: AsyncSession,
):
    stmt = (
        select(func.count())
        .select_from(ProductDealer)
        .filter(
            ProductDealer.status == match_status,
            and_(
                ProductDealer.created_at >= start_date if start_date else True,
                ProductDealer.created_at <= end_date if end_date else True,
            ),
        )
    )
    result_matching = await session.execute(stmt)
    count_matching = result_matching.scalar()
    return count_matching
