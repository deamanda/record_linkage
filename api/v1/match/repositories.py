from sqlalchemy import desc, or_, delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


from api.v1.match.depends import (
    matching,
    not_matching,
    matching_later,
    get_matched,
)
from api.v1.match.schemas import ProductDealerKey, ProductDealerKeyNone
from models import DealerPrice, User, Dealer
from models.match import ProductsMapped
from models.products import Product
from models.product_dealer import ProductDealer
from services.choices import SortedField


async def get_mapped(
    session: AsyncSession, count: int, dealerprice_id: int
) -> list[Product]:
    """Converting a list into products. Positioning"""
    products_id = await get_matched(
        session=session, count=count, dealerprice_id=dealerprice_id
    )
    stmt = select(Product)
    stmt = stmt.filter(Product.id.in_(products_id))
    result = await session.execute(stmt)
    selected_products = list(result.scalars().all())
    selected_products.sort(key=lambda x: products_id.index(x.id))
    mappeds = delete(ProductsMapped).where(
        ProductsMapped.dealerprice_id == dealerprice_id
    )
    await session.execute(mappeds)
    for index, product in enumerate(selected_products, start=1):
        product.position = index
        mapped = ProductsMapped(
            position=product.position,
            dealerprice_id=dealerprice_id,
            product_id=product.id,
        )
        session.add(mapped)
    await session.commit()
    await session.close()
    return selected_products


async def post_mapped(
    session: AsyncSession,
    mapped_in: ProductDealerKey,
    user: User,
):
    """Create Mapping"""
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
    """Create nor Mapping"""
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
    """Create deferred"""
    await matching_later(
        session=session,
        match_status="deferred",
        mapped_in=mapped_in,
        user=user,
    )
    return {"detail": "Match later."}


async def get_matcheds(
    session: AsyncSession,
    sort_by: SortedField | None,
    dealer_name: str | None,
    status: str | None,
    search_query: str | None,
    user_id: int | None = None,
    user: User | None = None,
):
    """Get all matched products"""
    stmt = (
        select(ProductDealer)
        .options(
            joinedload(ProductDealer.product),
            joinedload(ProductDealer.dealerprice).joinedload(
                DealerPrice.dealer
            ),
        )
        .outerjoin(DealerPrice, ProductDealer.key == DealerPrice.id)
        .outerjoin(Dealer, Dealer.id == DealerPrice.dealer_id)
        .filter(
            or_(ProductDealer.status == status, status is None),
            Dealer.name.ilike(f"%{dealer_name}%") if dealer_name else True,
            DealerPrice.product_name.ilike(f"%{search_query}%")
            if search_query
            else True,
        )
    )

    if user_id:
        stmt = stmt.filter(ProductDealer.user_id == user_id)
    elif user:
        user_local = await session.merge(user)
        stmt = stmt.filter(ProductDealer.user == user_local)

    if sort_by == "descending price":
        stmt = stmt.order_by(desc(DealerPrice.price))
    elif sort_by == "ascending price":
        stmt = stmt.order_by(DealerPrice.price)
    elif sort_by == "ascending time":
        stmt = stmt.order_by(ProductDealer.created_at)
    elif sort_by == "descending time":
        stmt = stmt.order_by(desc(ProductDealer.created_at))
    else:
        stmt = stmt.order_by(desc(ProductDealer.created_at))

    result = await session.execute(stmt)
    all_products = result.scalars().all()
    await session.close()
    return all_products
