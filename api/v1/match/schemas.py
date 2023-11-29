from datetime import datetime

from pydantic import BaseModel, conint

from api.v1.dealers.schemas import DealerPrice
from api.v1.products.schemas import Product


class ProductDealerKey(BaseModel):
    key: conint(gt=0)
    product_id: conint(gt=0)


class ProductDealer(BaseModel):
    product: Product
    dealerprice: DealerPrice
    created_at: datetime
