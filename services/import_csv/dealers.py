import csv
from models import DealerPrice, Dealer
from datetime import datetime


async def imports_dealerprice(file, session):
    """Importing dealer product data from CSV"""
    try:
        data = await file.read()
        decoded_data = data.decode("utf-8")

        csv_reader = csv.reader(decoded_data.splitlines(), delimiter=";")

        expected_columns = 7
        next(csv_reader)
        for row in csv_reader:
            if len(row) != expected_columns:
                print(f"Skipping row {len(row)}, incorrect number of values.")
                continue

            try:
                (
                    product_key,
                    price,
                    product_url,
                    product_name,
                    date,
                    dealer_id,
                ) = row
                product_data = {
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
            except ValueError as e:
                print(f"Error processing row {row}: {e}")

        await session.commit()
    finally:
        await session.close()


async def imports_dealers(file, session):
    """Importing dealers data from CSV"""
    try:
        data = await file.read()
        decoded_data = data.decode("utf-8")

        csv_reader = csv.reader(decoded_data.splitlines(), delimiter=";")

        expected_columns = 2
        next(csv_reader)
        for row in csv_reader:
            if len(row) != expected_columns:
                print(f"Skipping row {len(row)}, incorrect number of values.")
                continue

            try:
                (name) = row
                product_data = {"name": str(name)}

                product = Dealer(**product_data)
                session.add(product)
            except ValueError as e:
                print(f"Error processing row {row}: {e}")

        await session.commit()
    finally:
        await session.close()
