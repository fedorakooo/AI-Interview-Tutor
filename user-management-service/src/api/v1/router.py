from fastapi import APIRouter

from src.api.v1.endpoints.auth import router as auth_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
