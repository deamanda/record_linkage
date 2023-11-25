from typing import List
from repositories.products import ProductRepository
from schemas.products import Product


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def get_product(self) -> List[Product]:
        result = self.repository.get_product()
        return result

    def create_product(self) -> Product:
        result = self.repository.create_product()
        return result
