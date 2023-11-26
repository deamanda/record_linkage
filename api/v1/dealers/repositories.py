import math
from typing import Sequence

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.dealers import DealerPrice


async def get_dealerprice(
    session: AsyncSession, page: int, size: int
) -> dict[str, Sequence[DealerPrice] | dict[str, int]]:
    stmt = select(DealerPrice).order_by(DealerPrice.id)
    result = await session.execute(stmt)
    all_dealerprices = result.scalars().all()

    offset_min = (page - 1) * size
    offset_max = page * size
    paginated_dealerprice = all_dealerprices[offset_min:offset_max]
    pagination_info = {
        "page": page,
        "size": size,
        "total_pages": math.ceil(len(all_dealerprices) / size) - 1,
    }
    return {"pagination": pagination_info, "data": paginated_dealerprice}
