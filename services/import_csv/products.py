import csv

from sqlalchemy import select
from fastapi import HTTPException, status
from models import Product
from core.config import logger


async def imports_product(file, session):
    """Importing product data from CSV"""
    logger.info("Import product start.")
    try:
        data = await file.read()
        decoded_data = data.decode("utf-8")
        csv_reader = csv.reader(decoded_data.splitlines(), delimiter=";")
        expected_columns = 15
        first_row = next(csv_reader)

        if first_row[2] != "article":
            logger.warning(f"{file.filename} is not valid table.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Download a valid table. {file.filename} is not valid table.",
            )

        for row in csv_reader:
            if len(row) != expected_columns:
                logger.warning(
                    f"Skipping row {row}, incorrect number of values."
                )
                continue
            try:
                (
                    article,
                    ean_13,
                    name,
                    cost,
                    recommended_price,
                    category_id,
                    ozon_name,
                    name_1c,
                    wb_name,
                    ozon_article,
                    wb_article,
                    ym_article,
                    wb_article_td,
                ) = row[2:]
                existing_product = (
                    await session.execute(
                        select(Product).filter_by(article=article)
                    )
                ).scalar()

                if existing_product:
                    continue
                product_data = {
                    "article": article if article else None,
                    "ean_13": int(float(ean_13)) if ean_13 else None,
                    "name": name if name else None,
                    "cost": float(cost) if cost else None,
                    "recommended_price": float(recommended_price)
                    if recommended_price
                    else None,
                    "category_id": int(float(category_id))
                    if category_id
                    else None,
                    "ozon_name": ozon_name if ozon_name else None,
                    "name_1c": name_1c if name_1c else None,
                    "wb_name": wb_name if wb_name else None,
                    "ozon_article": ozon_article if ozon_article else None,
                    "wb_article": wb_article if wb_article else None,
                    "ym_article": ym_article if ym_article else None,
                    "wb_article_td": wb_article_td if wb_article_td else None,
                }
                product = Product(**product_data)
                session.add(product)
            except ValueError as e:
                logger.warning(f"Error processing row {row}: {e}")
        logger.info("Import product complete.")
        await session.commit()
    finally:
        await session.close()
