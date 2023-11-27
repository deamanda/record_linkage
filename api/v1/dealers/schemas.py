from typing import List

from pydantic import BaseModel, ConfigDict, AnyUrl, computed_field
from datetime import date

from services.pagination import Pagination


class DealerPriceBase(BaseModel):
    id: int
    product_key: int | None
    price: float | None
    product_url: AnyUrl | None
    product_name: str | None
    date: date
    dealer_id: int | None
    mapped: bool | None

    @computed_field
    @property
    def mapped_products(self) -> List[list[int]]:
        return [[23]]

    class Config:
        json_encoders = {date: lambda v: v.strftime("%d.%m.%Y")}


class DealerPrice(DealerPriceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Dealer(BaseModel):
    id: int
    name: str


class DealerPriceResponse(BaseModel):
    pagination: Pagination
    data: List[DealerPrice]


class DealerResponse(BaseModel):
    pagination: Pagination
    data: List[Dealer]
