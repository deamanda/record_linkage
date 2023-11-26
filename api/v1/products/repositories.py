from typing import Sequence

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.products import Product
from services.pagination import pagination


async def get_products(
    session: AsyncSession, page: int, size: int
) -> dict[str, Sequence[Product] | dict[str, int]]:
    stmt = select(Product).order_by(Product.id)
    result = await session.execute(stmt)
    all_products = result.scalars().all()
    return pagination(page, size, all_products)


async def get_product(
    session: AsyncSession, product_id: int
) -> Product | None:
    return await session.get(Product, product_id)
