from api.v1.repositories.products import ProductRepository
from api.v1.services.products import ProductService


product_repository = ProductRepository()

product_service = ProductService(product_repository)


def get_product_service() -> ProductService:
    return product_service
