from typing import List
from schemas.products import Product


class ProductRepository:
    def get_product(self) -> List[Product]:
        ...

    def create_product(self) -> Product:
        ...
