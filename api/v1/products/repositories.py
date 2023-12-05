from typing import Sequence

from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import ModelVector
from models.products import Product
from services.match import create_embeddings


async def get_products(
    session: AsyncSession, search_query: str
) -> Sequence[Product]:
    """Getting a list of products"""
    stmt = select(Product).filter(
        Product.name.ilike(f"%{search_query}%") if search_query else True,
    )
    result = await session.execute(stmt)
    all_products = result.scalars().all()
    await session.close()
    return all_products


async def get_product(
    session: AsyncSession, product_id: int
) -> Product | None:
    """Receiving goods by ID"""
    return await session.get(Product, product_id)


async def model_training(
    session: AsyncSession,
):
    """Product training function"""
    result = await session.execute(select(Product.name))
    product_names = [row[0] for row in result]
    vectors_list = create_embeddings(product_names)
    python_list = vectors_list.tolist()
    stmt = delete(ModelVector)
    await session.execute(stmt)
    for inner_list in python_list:
        model_instance = ModelVector(value=inner_list)
        session.add(model_instance)
    await session.commit()
    await session.close()
