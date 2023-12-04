from enum import Enum

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.db_helper import db_helper
from models import ProductDealer

ALLOWED_SORT_FIELDS = ["deferred", "not matched", "matched"]


async def validate_availability_check(
    model,
    value: int,
    session: AsyncSession,
    message: str,
):
    data = select(model).where(model.id == value)
    results = await session.execute(data)
    result = results.scalar()
    if not result:
        await session.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{message} with id={value} not found.",
        )


async def pre_dealer_price_validate(
    mapped_in,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    dealer_price = select(ProductDealer).where(
        ProductDealer.key == mapped_in.key
    )
    result = await session.execute(dealer_price)
    if result.scalar():
        await session.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item has already been matched!",
        )


class MatchingStatus(str, Enum):
    option1 = "not matched"
    option2 = "matched"
    option3 = "deferred"


class DealerPriceStatus(str, Enum):
    option1 = "not matched"
    option2 = "matched"
    option3 = "deferred"
    option4 = "not processed"
