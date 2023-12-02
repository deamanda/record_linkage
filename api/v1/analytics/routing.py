from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query

from api.v1.analytics.repositories import get_compared
from api.v1.analytics.schemas import MatchedCount

from core.db_helper import db_helper


router = APIRouter(prefix="/analytics", tags=["Аналитика"])


@router.get(
    "/matched-count",
    response_model=MatchedCount,
    summary="Общее количество сопоставлений",
)
async def get_times_compared(
    start_date: datetime = Query(
        default=datetime.now() - timedelta(days=365), description="Start date"
    ),
    end_date: datetime = Query(default=datetime.now(), description="End date"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_compared(
        session=session, start_date=start_date, end_date=end_date
    )
    return value
