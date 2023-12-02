import random
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
from api.v1.products.depends import product_by_id
from api.v1.products.schemas import Product
from core.auth import fastapi_users

from core.db_helper import db_helper
from fastapi import Query

from models import User
from services.validators import MatchingStatus

router = APIRouter(prefix="/matching", tags=["Сопоставление"])
current_active_user = fastapi_users.current_user(active=True)


@router.get(
    "/all",
    summary="Получить все сопоставленные товары",
    response_model=LimitOffsetPage[ProductDealer],
)
async def get_matched(
    search_query: str = Query(default=None, description="Search"),
    status: MatchingStatus = Query(
        default=None, description="Matching status"
    ),
    sort_by_time: bool = Query(default=None, description="Sort by time"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_matcheds(
        session=session,
        sort_by_time=sort_by_time,
        status=status,
        search_query=search_query,
        user_id=None,
        user=None,
    )
    return paginate(value)


@router.get(
    "/{dealerprice_id}/",
    summary="Получить сопоставляемые товары заказчика",
    response_model=List[Product],
)
async def get_mapped_products(
    count: int = Query(ge=1, le=25, default=5),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    product: Product = Depends(product_by_id),
):
    print(product)  # будет передаваться в match
    products_id = [random.randint(1, 300) for _ in range(count)]
    return await get_mapped(session=session, products_id=products_id)


@router.get(
    "/user/me",
    summary="Получить сопоставленные товары текущего юзера",
    response_model=LimitOffsetPage[ProductDealer],
)
async def get_matched(
    search_query: str = Query(default=None, description="Search"),
    status: MatchingStatus = Query(
        default=None, description="Matching status"
    ),
    user: User = Depends(current_active_user),
    sort_by_time: bool = Query(default=None, description="Sort by time"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_matcheds(
        session=session,
        sort_by_time=sort_by_time,
        status=status,
        search_query=search_query,
        user_id=None,
        user=user,
    )
    return paginate(value)


@router.get(
    "/user/{user_id}",
    summary="Получить сопоставленные товары конеретного юзера",
    response_model=LimitOffsetPage[ProductDealer],
)
async def get_matched(
    user_id: int,
    search_query: str = Query(default=None, description="Search"),
    status: MatchingStatus = Query(
        default=None, description="Matching status"
    ),
    sort_by_time: bool = Query(default=None, description="Sort by time"),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    value = await get_matcheds(
        session=session,
        sort_by_time=sort_by_time,
        status=status,
        search_query=search_query,
        user_id=user_id,
        user=None,
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
