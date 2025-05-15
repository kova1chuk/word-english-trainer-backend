from fastapi import APIRouter
from .auth import router as auth_router
from .words import router as words_router
from .health import router as health_router
from .dictionary import router as dictionary_router
from .profile import router as profile_router

router = APIRouter()

router.include_router(health_router)
router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(words_router)
router.include_router(dictionary_router)
