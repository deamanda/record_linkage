from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


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
