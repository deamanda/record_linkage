import math
from typing import Sequence

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.products import Product


async def get_products(
    session: AsyncSession, page: int, size: int
) -> dict[str, Sequence[Product] | dict[str, int]]:
    stmt = select(Product).order_by(Product.id)
    result = await session.execute(stmt)
    all_products = result.scalars().all()

    offset_min = (page - 1) * size
    offset_max = page * size
    paginated_products = all_products[offset_min:offset_max]
    pagination_info = {
        "page": page,
        "size": size,
        "total_pages": math.ceil(len(all_products) / size) - 1,
    }
    return {"pagination": pagination_info, "data": paginated_products}
