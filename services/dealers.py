import csv
from models import Product


async def imports_dealerprice(file, session):
    try:
        data = await file.read()
        decoded_data = data.decode("utf-8")

        csv_reader = csv.reader(decoded_data.splitlines(), delimiter=";")

        expected_columns = 15
        next(csv_reader)
        for row in csv_reader:
            if len(row) != expected_columns:
                print(f"Skipping row {len(row)}, incorrect number of values.")
                continue

            try:
                (
                    id,
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
                ) = row[1:]
                product_data = {
                    "id": int(id),
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
                print(f"Error processing row {row}: {e}")

        await session.commit()
    finally:
        await session.close()
