from fastapi import APIRouter

from app.api.v1.category_router import router as category_router
from app.api.v1.product_router import router as product_router
from app.api.v1.product_variant_router import router as product_variant_router
from app.core.config import get_settings

settings = get_settings()
router = APIRouter()


@router.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "env": settings.ENV,
    }


router.include_router(category_router)
router.include_router(product_router)
router.include_router(product_variant_router)
