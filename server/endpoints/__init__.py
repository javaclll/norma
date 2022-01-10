from fastapi import APIRouter

from .health_endpoint import router as health_endpoint_router
from .statics import router as statics_router


router = APIRouter()

router.include_router(health_endpoint_router)
router.include_router(statics_router)
