from fastapi import APIRouter

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
