from fastapi import APIRouter

from .auth import router as auth_router
from .copy_injection import router as copy_injection_router
from .health import router as health_router
from .user import router as user_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(copy_injection_router, prefix="/agents", tags=["agents"])
