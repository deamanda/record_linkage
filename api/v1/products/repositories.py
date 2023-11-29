from typing import Sequence

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.products import Product


async def get_products(session: AsyncSession) -> Sequence[Product]:
    stmt = select(Product).order_by(Product.id)
    result = await session.execute(stmt)
    all_products = result.scalars().all()
    return all_products


async def get_product(
    session: AsyncSession, product_id: int
) -> Product | None:
    return await session.get(Product, product_id)
