from pydantic import BaseModel


class ProductDealerKey(BaseModel):
    key: int
    product_id: int
    dealer_id: int
