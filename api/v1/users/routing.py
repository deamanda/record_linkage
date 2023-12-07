from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query

from api.v1.users.repositories import get_users
from api.v1.users.schemas import UserAll
from core.db_helper import db_helper
from fastapi_pagination import LimitOffsetPage, paginate


router = APIRouter(prefix="/users", tags=["Пользователь"])


@router.get(
    "/all",
    response_model=LimitOffsetPage[UserAll],
    summary="Получить всех пользователей",
)
async def get_all_products(
    search_query: str = Query(default=None, description="Search"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_users(session=session, search_query=search_query)
    return paginate(value)
