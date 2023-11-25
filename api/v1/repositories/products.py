from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.products import Product


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(
    session: AsyncSession, product_id: int
) -> Product | None:
    return await session.get(Product, product_id)
