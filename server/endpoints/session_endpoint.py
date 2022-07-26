from fastapi import APIRouter
from fastapi.responses import JSONResponse

from core.ident import generate_new_identity

router = APIRouter()


@router.post("/ident")
async def new_identity():
    new_ident = generate_new_identity()
    return JSONResponse(
        content={"success": True, "ident": new_ident},
        media_type="application/json",
    )
