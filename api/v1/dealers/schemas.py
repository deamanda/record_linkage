from pydantic import BaseModel, ConfigDict, AnyUrl
from datetime import date


class DealerPriceBase(BaseModel):
    id: int
    product_key: int | None
    price: float | None
    product_url: AnyUrl | None
    product_name: str | None
    date: date
    dealer_id: int | None

    class Config:
        json_encoders = {date: lambda v: v.strftime("%d.%m.%Y")}


class DealerPrice(DealerPriceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class Dealer(BaseModel):
    id: int
    name: str
