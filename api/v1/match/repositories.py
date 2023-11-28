from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.products import Product


async def get_mapped(session: AsyncSession, products_id) -> list[Product]:
    stmt = select(Product)
    stmt = stmt.filter(Product.id.in_(products_id))
    result = await session.execute(stmt)
    selected_products = list(result.scalars().all())
    selected_products.sort(key=lambda x: products_id.index(x.id))
    return selected_products
