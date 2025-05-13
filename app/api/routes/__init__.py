from fastapi import APIRouter
from .auth import router as auth_router
from .words import router as words_router
from .health import router as health_router

router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["Health"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(words_router, prefix="/words", tags=["Words"])
