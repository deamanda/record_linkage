from typing import List

from pydantic import BaseModel, ConfigDict

from services.pagination import Pagination


class ProductBase(BaseModel):
    id: int
    article: str | None
    ean_13: int | None
    name: str | None
    cost: float | None
    recommended_price: float | None
    category_id: int | None
    ozon_name: str | None
    name_1c: str | None
    wb_name: str | None
    ozon_article: str | None
    wb_article: str | None
    ym_article: str | None


class Product(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProductResponse(BaseModel):
    pagination: Pagination
    data: List[Product]
