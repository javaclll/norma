from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health")
async def health_check() -> Any:
    return JSONResponse(content={"status": "ok"}, media_type="application/health+json")
