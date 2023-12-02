from datetime import datetime

from pydantic import BaseModel, conint

from api.v1.dealers.schemas import DealerPrice
from api.v1.products.schemas import ProductSmall


class ProductDealerKey(BaseModel):
    key: conint(gt=0)
    product_id: conint(gt=0)


class ProductDealerNone(BaseModel):
    dealerprice: DealerPrice
    created_at: datetime
    status: str | None

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%d.%m.%Y %H:%M:%S")}


class ProductDealer(ProductDealerNone):
    product: ProductSmall | None


class ProductDealerKeyNone(BaseModel):
    key: conint(gt=0)
