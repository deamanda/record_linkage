from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.match.depends import product_dealer_validate
from api.v1.match.schemas import ProductDealerKey
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
    session: AsyncSession, mapped_in: ProductDealerKey
) -> ProductDealer:
    await product_dealer_validate(session=session, mapped_in=mapped_in)
    mapped = ProductDealer(**mapped_in.model_dump())
    session.add(mapped)
    await session.commit()
    return mapped
