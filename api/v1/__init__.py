from fastapi import APIRouter

from .products.routing import router as products_router
from .dealers.routing import router as dealers_router

router = APIRouter(prefix="/v1")
router.include_router(router=products_router)
router.include_router(router=dealers_router)
