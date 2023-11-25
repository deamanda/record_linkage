from typing import List
from api.v1.schemas.products import Product


class ProductRepository:
    def get_product(self) -> List[Product]:
        ...

    def create_product(self) -> Product:
        ...
