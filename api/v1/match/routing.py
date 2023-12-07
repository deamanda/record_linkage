from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi_pagination import LimitOffsetPage, paginate

from api.v1.match.repositories import (
    get_mapped,
    post_mapped,
    get_matcheds,
    post_not_mapped,
    post_mapped_later,
)
from api.v1.match.schemas import (
    ProductDealerKey,
    ProductDealer,
    ProductDealerKeyNone,
)
from api.v1.products.schemas import ProductSmall
from core.auth import fastapi_users
from core.config import logger

from core.db_helper import db_helper
from fastapi import Query

from models import User
from services.choices import MatchingStatus, SortedField

router = APIRouter(prefix="/matching", tags=["Сопоставление"])
current_active_user = fastapi_users.current_user(active=True)


@router.get(
    "/all",
    summary="Получить все сопоставленные товары",
    response_model=LimitOffsetPage[ProductDealer],
)
async def get_matched(
    dealer_name: str = Query(default=None, description="Dealer"),
    search_query: str = Query(default=None, description="Search"),
    status: MatchingStatus = Query(
        default=None, description="Matching status"
    ),
    sort_by: SortedField = Query(default=None, description="Sort by"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_matcheds(
        session=session,
        sort_by=sort_by,
        status=status,
        search_query=search_query,
        user_id=None,
        user=None,
        dealer_name=dealer_name,
    )
    return paginate(value)


@router.get(
    "/{dealerprice_id}/",
    summary="Получить сопоставляемые товары заказчика",
    response_model=List[ProductSmall],
)
async def get_mapped_products(
    dealerprice_id: int,
    count: int = Query(ge=1, le=25, default=5),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    logger.info("Receiving matched products.")
    return await get_mapped(
        session=session, dealerprice_id=dealerprice_id, count=count
    )


@router.get(
    "/user/me",
    summary="Получить сопоставленные товары текущего юзера",
    response_model=LimitOffsetPage[ProductDealer],
)
async def get_matched(
    dealer_name: str = Query(default=None, description="Dealer"),
    search_query: str = Query(default=None, description="Search"),
    status: MatchingStatus = Query(
        default=None, description="Matching status"
    ),
    user: User = Depends(current_active_user),
    sort_by: SortedField = Query(default=None, description="Sort by"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_matcheds(
        session=session,
        sort_by=sort_by,
        status=status,
        search_query=search_query,
        user=user,
        dealer_name=dealer_name,
    )
    return paginate(value)


@router.get(
    "/user/{user_id}",
    summary="Получить сопоставленные товары конеретного юзера",
    response_model=LimitOffsetPage[ProductDealer],
)
async def get_matched(
    user_id: int,
    dealer_name: str = Query(default=None, description="Dealer"),
    search_query: str = Query(default=None, description="Search"),
    status: MatchingStatus = Query(
        default=None, description="Matching status"
    ),
    sort_by: SortedField = Query(default=None, description="Sort by"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_matcheds(
        session=session,
        sort_by=sort_by,
        status=status,
        search_query=search_query,
        user_id=user_id,
        dealer_name=dealer_name,
    )
    return paginate(value)


@router.post(
    "/accepted",
    summary="Сопоставить товары (есть сопоставление)",
    response_model=dict,
)
async def post_mapped_products(
    mapped_in: ProductDealerKey,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await post_mapped(session=session, mapped_in=mapped_in, user=user)


@router.post(
    "/not-accepted",
    summary="Сопоставить товары (нет сопоставления)",
    response_model=dict,
)
async def post_not_mapped_products(
    mapped_in: ProductDealerKeyNone,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await post_not_mapped(
        session=session, mapped_in=mapped_in, user=user
    )


@router.post(
    "/accepted-later",
    summary="Сопоставить товары (отложить)",
    response_model=dict,
)
async def post_mapped_products_later(
    mapped_in: ProductDealerKeyNone,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await post_mapped_later(
        session=session, mapped_in=mapped_in, user=user
    )
