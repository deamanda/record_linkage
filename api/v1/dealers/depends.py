from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path
from typing import Annotated

from api.v1.dealers.repositories import get_dealerprice

from core.db_helper import db_helper


from models import DealerPrice


async def dealerprice_by_id(
    dealerprice_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> DealerPrice:
    dealerprice = await get_dealerprice(
        session=session, dealerprice_id=dealerprice_id
    )
    if dealerprice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dealer product with id = {dealerprice_id} not found.",
        )
    return dealerprice
