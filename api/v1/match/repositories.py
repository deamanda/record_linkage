from sqlalchemy import desc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


from api.v1.match.depends import matching, not_matching, matching_later
from api.v1.match.schemas import ProductDealerKey, ProductDealerKeyNone
from models.products import Product
from models.product_dealer import ProductDealer


async def get_mapped(session: AsyncSession, products_id) -> list[Product]:
    stmt = select(Product)
    stmt = stmt.filter(Product.id.in_(products_id))
    result = await session.execute(stmt)
    selected_products = list(result.scalars().all())
    selected_products.sort(key=lambda x: products_id.index(x.id))
    return selected_products


async def post_mapped(session: AsyncSession, mapped_in: ProductDealerKey):
    await matching(
        session=session,
        match_status=True,
        mapped_in=mapped_in,
    )
    return {"detail": "Match found."}


async def post_not_mapped(
    session: AsyncSession, mapped_in: ProductDealerKeyNone
):
    await not_matching(
        session=session,
        match_status=False,
        mapped_in=mapped_in,
    )
    return {"detail": "No match found."}


async def post_mapped_later(
    session: AsyncSession, mapped_in: ProductDealerKeyNone
):
    await matching_later(
        session=session,
        match_status=None,
        mapped_in=mapped_in,
    )
    return {"detail": "Match later."}


async def get_matcheds(session: AsyncSession):
    stmt = (
        select(ProductDealer)
        .options(
            joinedload(ProductDealer.product),
            joinedload(ProductDealer.dealerprice),
        )
        .order_by(desc(ProductDealer.created_at))
    )

    result = await session.execute(stmt)
    all_products = result.scalars().all()
    return all_products
