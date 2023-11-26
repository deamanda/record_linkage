from typing import List

from pydantic import BaseModel, ConfigDict, AnyUrl
from datetime import date

from services.pagination import Pagination


class DealerPriceBase(BaseModel):
    id: int
    product_key: int | None
    price: float | None
    product_url: AnyUrl | None
    product_name: str | None
    date: date | None
    dealer_id: int | None


class DealerPrice(DealerPriceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Dealer(BaseModel):
    id: str
    name: str


class DealerPriceResponse(BaseModel):
    pagination: Pagination
    data: List[DealerPrice]
