from typing import Sequence

from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import ModelVector
from models.products import Product
from services.DS_match.match import norm_name, create_embeddings


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
    result = await session.execute(select(Product.id, Product.name_1c))
    product_info = [
        [
            row[0],
            norm_name(row[1])[1] if row[1] else row[1],
            norm_name(row[1])[0] if row[1] else row[1],
        ]
        for row in result
    ]

    product_names = [row[2] for row in product_info]
    vector_names = create_embeddings(product_names)
    stmt = delete(ModelVector)
    await session.execute(stmt)
    for i, row in enumerate(product_info):
        model_instance = ModelVector(
            value=vector_names[i],
            product_key=row[0],
            size=row[1],
        )
        session.add(model_instance)
    await session.commit()
    await session.close()
