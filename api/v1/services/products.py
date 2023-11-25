from typing import List
from api.v1.repositories.products import ProductRepository
from api.v1.schemas.products import Product


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def get_product(self) -> List[Product]:
        result = self.repository.get_product()
        return result

    def create_product(self) -> Product:
        result = self.repository.create_product()
        return result
