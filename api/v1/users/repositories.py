from typing import Sequence

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User


async def get_users(
    session: AsyncSession, search_query: str
) -> Sequence[User]:
    stmt = select(User).filter(
        User.username.ilike(f"%{search_query}%") if search_query else True,
    )
    result = await session.execute(stmt)
    all_users = result.scalars().all()
    await session.close()
    return all_users
