from enum import Enum

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


ALLOWED_SORT_FIELDS = ["deferred", "not matched", "matched"]


async def validate_availability_check(
    model,
    value: int,
    session: AsyncSession,
    message: str,
):
    """Validator for checking a field by ID"""
    data = select(model).where(model.id == value)
    results = await session.execute(data)
    result = results.scalar()
    if not result:
        await session.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{message} with id={value} not found.",
        )


class MatchingStatus(str, Enum):
    """Selecting a filter for matched products"""

    option1 = "not matched"
    option2 = "matched"
    option3 = "deferred"


class DealerPriceStatus(str, Enum):
    """Selecting a filter for dealer products"""

    option1 = "not matched"
    option2 = "matched"
    option3 = "deferred"
    option4 = "not processed"
