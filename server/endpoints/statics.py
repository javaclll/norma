from typing import Any

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/statics/swagger-ui-bundle.js", include_in_schema=False)
async def swagger_ui_bundle() -> Any:
    return FileResponse("statics/swagger-ui-bundle.js")

@router.get("/statics/swagger-ui.css", include_in_schema=False)
async def swagger_ui_css() -> Any:
    return FileResponse("statics/swagger-ui.css")
