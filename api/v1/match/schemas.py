from pydantic import BaseModel, conint


class ProductDealerKey(BaseModel):
    key: conint(gt=0)
    product_id: conint(gt=0)
