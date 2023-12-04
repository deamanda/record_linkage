from sqlalchemy import desc, or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


from api.v1.match.depends import matching, not_matching, matching_later
from api.v1.match.schemas import ProductDealerKey, ProductDealerKeyNone
from models import DealerPrice, User
from models.products import Product
from models.product_dealer import ProductDealer


async def get_mapped(session: AsyncSession, products_id) -> list[Product]:
    stmt = select(Product)
    stmt = stmt.filter(Product.id.in_(products_id))
    result = await session.execute(stmt)
    selected_products = list(result.scalars().all())
    selected_products.sort(key=lambda x: products_id.index(x.id))
    return selected_products


async def post_mapped(
    session: AsyncSession,
    mapped_in: ProductDealerKey,
    user: User,
):
    await matching(
        session=session,
        match_status="matched",
        mapped_in=mapped_in,
        user=user,
    )
    return {"detail": "Match found."}


async def post_not_mapped(
    session: AsyncSession,
    mapped_in: ProductDealerKeyNone,
    user: User,
):
    await not_matching(
        session=session,
        match_status="not matched",
        mapped_in=mapped_in,
        user=user,
    )
    return {"detail": "No match found."}


async def post_mapped_later(
    session: AsyncSession,
    mapped_in: ProductDealerKeyNone,
    user: User,
):
    await matching_later(
        session=session,
        match_status="deferred",
        mapped_in=mapped_in,
        user=user,
    )
    return {"detail": "Match later."}


async def get_matcheds(
    session: AsyncSession,
    sort_by_time: bool | None,
    status: str | None,
    search_query: str | None,
    user_id: int | None = None,
    user: User | None = None,
    dealer_id: int | None = None,
):
    stmt = (
        select(ProductDealer)
        .options(
            joinedload(ProductDealer.product),
            joinedload(ProductDealer.dealerprice).joinedload(
                DealerPrice.dealer
            ),
        )
        .outerjoin(DealerPrice, ProductDealer.key == DealerPrice.id)
        .filter(
            or_(ProductDealer.status == status, status is None),
            DealerPrice.product_name.ilike(f"%{search_query}%")
            if search_query
            else True,
        )
        .order_by(
            desc(ProductDealer.created_at)
            if sort_by_time
            else ProductDealer.created_at
        )
    )

    if user_id:
        stmt = stmt.filter(ProductDealer.user_id == user_id)
    elif user:
        user_local = await session.merge(user)
        stmt = stmt.filter(ProductDealer.user == user_local)
    elif dealer_id:
        stmt = stmt.filter(ProductDealer.dealer_id == dealer_id)

    result = await session.execute(stmt)
    all_products = result.scalars().all()
    await session.close()
    return all_products
