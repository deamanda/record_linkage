import csv

from sqlalchemy import select, func
from fastapi import HTTPException, status

from core.config import logger
from models import DealerPrice, Dealer
from datetime import datetime


async def imports_dealerprice(file, session):
    """Importing dealer product data from CSV"""
    logger.info("Import dealer price start.")
    try:
        data = await file.read()
        decoded_data = data.decode("utf-8")
        csv_reader = csv.reader(decoded_data.splitlines(), delimiter=";")
        expected_columns = 7
        first_row = next(csv_reader)

        if first_row[1] != "product_key":
            logger.warning(f"{file.filename} is not valid table.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Download a valid table. {file.filename} is not valid table.",
            )

        max_id = await session.execute(select(func.max(DealerPrice.id)))
        max_id_value = max_id.scalar() or 0
        starting_id = max_id_value + 1

        for row in csv_reader:
            if len(row) != expected_columns:
                logger.warning(
                    f"Skipping row {len(row)}, incorrect number of values."
                )
                continue

            try:
                (
                    product_key,
                    price,
                    product_url,
                    product_name,
                    date,
                    dealer_id,
                ) = row[1:]

                product_data = {
                    "id": starting_id,
                    "product_key": product_key if product_key else None,
                    "price": float(price) if price else None,
                    "product_url": product_url if product_url else None,
                    "product_name": product_name if product_name else None,
                    "date": datetime.strptime(date, "%Y-%m-%d")
                    if date
                    else None,
                    "dealer_id": int(dealer_id) if dealer_id else None,
                }
                product = DealerPrice(**product_data)
                session.add(product)
                starting_id += 1
            except ValueError as e:
                logger.warning(f"Error processing row {row}: {e}")

        logger.info("Import dealer price complete.")
        await session.commit()
    finally:
        await session.close()


async def imports_dealers(file, session):
    """Importing dealers data from CSV"""
    logger.info("Import dealers start.")
    try:
        data = await file.read()
        decoded_data = data.decode("utf-8")
        csv_reader = csv.reader(decoded_data.splitlines(), delimiter=";")
        expected_columns = 2
        first_row = next(csv_reader)

        if first_row[1] != "name":
            logger.warning(f"{file.filename} is not valid table.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Download a valid table. {file.filename} is not valid table.",
            )

        for row in csv_reader:
            if len(row) != expected_columns:
                logger.warning(
                    f"Skipping row {len(row)}, incorrect number of values."
                )
                continue
            try:
                id, name = row
                existing_product = (
                    await session.execute(
                        select(Dealer).filter_by(name=name, id=int(id))
                    )
                ).scalar()

                if existing_product:
                    continue
                product = Dealer(id=int(id), name=name)
                session.add(product)
            except ValueError as e:
                logger.warning(f"Error processing row {row}: {e}")

        logger.info("Import dealers complete.")
        await session.commit()
    finally:
        await session.close()
