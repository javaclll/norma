from fastapi import APIRouter

from .health_endpoint import router as health_endpoint_router
from .statics import router as statics_router
from .game_endpoint import router as game_endpoint_router
from .session_endpoint import router as session_endpoint_router


router = APIRouter()

router.include_router(health_endpoint_router)
router.include_router(statics_router)
router.include_router(session_endpoint_router)
router.include_router(game_endpoint_router)
