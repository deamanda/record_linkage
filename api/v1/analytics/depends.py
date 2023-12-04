from datetime import datetime

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models import ProductDealer, Dealer, User
from services.validators import validate_availability_check


async def count_match(
    match_status: str,
    start_date: datetime,
    end_date: datetime,
    session: AsyncSession,
    user=None,
    dealer_id: int = None,
    user_id: int = None,
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

    if user:
        stmt = stmt.filter(ProductDealer.user == user)
    elif dealer_id:
        await validate_availability_check(Dealer, dealer_id, session, "Dealer")
        stmt = stmt.filter(ProductDealer.dealer_id == dealer_id)
    elif user_id:
        await validate_availability_check(User, user_id, session, "User")
        stmt = stmt.filter(ProductDealer.user_id == user_id)

    result_matching = await session.execute(stmt)
    count_matching = result_matching.scalar()
    await session.close()
    return count_matching


async def get_position_statistics(
    start_date: datetime,
    end_date: datetime,
    session: AsyncSession,
    user=None,
    dealer_id: int = None,
    user_id: int = None,
):
    stmt = (
        select(ProductDealer.position, func.count().label("position_count"))
        .filter(
            ProductDealer.position.isnot(None),
            and_(
                ProductDealer.created_at >= start_date if start_date else True,
                ProductDealer.created_at <= end_date if end_date else True,
            ),
        )
        .group_by(ProductDealer.position)
        .order_by(ProductDealer.position)
    )

    if user:
        stmt = stmt.filter(ProductDealer.user == user)
    elif dealer_id:
        await validate_availability_check(Dealer, dealer_id, session, "Dealer")
        stmt = stmt.filter(ProductDealer.dealer_id == dealer_id)
    elif user_id:
        await validate_availability_check(User, user_id, session, "User")
        stmt = stmt.filter(ProductDealer.user_id == user_id)

    result = await session.execute(stmt)
    statistics = result.all()

    total_positions = sum(stat.position_count for stat in statistics)
    position_percentages = [
        {
            "position": stat.position,
            "percentage": (stat.position_count / total_positions) * 100,
        }
        for stat in statistics
    ]
    return position_percentages
