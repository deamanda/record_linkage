from pydantic import BaseModel
from datetime import datetime


class Product(BaseModel):
    article: str
    ean_13: int
    name: str
    cost: int
    min_recommended_price: int
    recommended_price: int
    category_id: int
    ozon_name: str
    name_1c: str
    wb_name: str
    ozon_article: str
    wb_article: str
    ym_article: str


class DealerPrice(BaseModel):
    product_key: int
    price: int
    product_url: str  # Заменить на урл
    product_name: str
    date: datetime
    dealer_id: int


class Dealer(BaseModel):
    name: str
