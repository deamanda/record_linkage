from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query

from api.v1.analytics.repositories import get_compared
from api.v1.analytics.schemas import MatchedCount
from core.auth import fastapi_users

from core.db_helper import db_helper
from models import User

router = APIRouter(prefix="/analytics", tags=["Аналитика"])
current_active_user = fastapi_users.current_user(active=True)


@router.get(
    "/matched-count/dealer/{dealer_id}",
    response_model=MatchedCount,
    summary="Количество сопоставлений для конкретного дилера",
)
async def get_times_compared(
    dealer_id: int,
    start_date: datetime = Query(
        default=datetime.now() - timedelta(days=365), description="Start date"
    ),
    end_date: datetime = Query(default=datetime.now(), description="End date"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_compared(
        session=session,
        start_date=start_date,
        end_date=end_date,
        dealer_id=dealer_id,
    )
    return value


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


@router.get(
    "/matched-count/user/me",
    response_model=MatchedCount,
    summary="Количество сопоставлений текущего юзера",
)
async def get_times_compared(
    start_date: datetime = Query(
        default=datetime.now() - timedelta(days=365), description="Start date"
    ),
    end_date: datetime = Query(default=datetime.now(), description="End date"),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_compared(
        session=session,
        start_date=start_date,
        end_date=end_date,
        user=user,
    )
    return value


@router.get(
    "/matched-count/user/{user_id}",
    response_model=MatchedCount,
    summary="Количество сопоставлений текущего юзера",
)
async def get_times_compared(
    user_id: int,
    start_date: datetime = Query(
        default=datetime.now() - timedelta(days=365), description="Start date"
    ),
    end_date: datetime = Query(default=datetime.now(), description="End date"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_compared(
        session=session,
        start_date=start_date,
        end_date=end_date,
        user_id=user_id,
    )
    return value
