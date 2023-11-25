from pydantic import BaseModel
from datetime import datetime


class DealerPrice(BaseModel):
    product_key: int
    price: int
    product_url: str  # Заменить на урл
    product_name: str
    date: datetime
    dealer_id: int


class Dealer(BaseModel):
    name: str
