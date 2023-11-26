from typing import List

from pydantic import BaseModel, ConfigDict, AnyUrl
from datetime import date
from typing import Any, ClassVar

from services.pagination import Pagination


class DealerPriceBase(BaseModel):
    id: int
    product_key: int | None
    price: float | None
    product_url: AnyUrl | None
    product_name: str | None
    date: date
    dealer_id: int | None
    example_data: ClassVar[dict[str, Any]] = {
        "name": "John Doe",
        "date_of_birth": "15-Jul-1996",
        "gender": "m",
    }

    class Config:
        json_encoders = {date: lambda v: v.strftime("%d.%m.%Y")}


class DealerPrice(DealerPriceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Dealer(BaseModel):
    id: str
    name: str


class DealerPriceResponse(BaseModel):
    pagination: Pagination
    data: List[DealerPrice]
