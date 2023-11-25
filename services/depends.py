from repositories.products import ProductRepository
from services.products import ProductService


product_repository = ProductRepository()

product_service = ProductService(product_repository)


def get_product_service() -> ProductService:
    return product_service
