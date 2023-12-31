from pydantic import BaseModel, ConfigDict


class ProductSmall(BaseModel):
    id: int
    name: str | None
    article: str | None
    recommended_price: float | None
    cost: float | None


class ProductBase(ProductSmall):
    ean_13: int | None
    category_id: int | None
    ozon_name: str | None
    name_1c: str | None
    wb_name: str | None
    ozon_article: str | None
    wb_article: str | None
    ym_article: str | None


class Product(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
