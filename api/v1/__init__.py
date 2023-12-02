from fastapi import APIRouter

from .products.routing import router as products_router
from .dealers.routing import router as dealers_router
from .match.routing import router as match_router
from .analytics.routing import router as analytics_router
from .users.routing import router as users_router

router = APIRouter(prefix="/v1")
router.include_router(router=products_router)
router.include_router(router=dealers_router)
router.include_router(router=match_router)
router.include_router(router=analytics_router)
router.include_router(router=users_router)
