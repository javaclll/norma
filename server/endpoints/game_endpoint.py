import random
from typing import Any, Optional

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic.networks import ascii_domain_regex

from core.ident import Ident, get_ident
from core.socket import manager

router = APIRouter()


@router.post("/create-game")
async def create_game(
    ident: Ident = Depends(get_ident),
    preference: Optional[int] = None,  # -1 for Tiger and 1 for Goat
) -> Any:
    if preference in [-1, 1]:
        piece = preference
    else:
        piece = random.choice([-1, 1])

    game_id = manager.create_game()

    manager.assign_game(game_id, ident.value, piece)

    return JSONResponse(
        content={"success": True, "piece": piece, "game_id": game_id},
    )


@router.websocket("/game")
async def game(
    websocket: WebSocket,
    id: str,
    ident: str,
) -> Any:
    await manager.connect(websocket, ident, id)
    try:
        while True:
            message = await websocket.receive_json()
            await manager.handle_messages(message, ident, id, websocket)
    except WebSocketDisconnect:
        manager.disconnect(id, websocket)

@router.websocket("/glory")
async def game(
    websocket: WebSocket,
    id: str,
    ident: str,
) -> Any:
    await manager.executor_connect(websocket, ident)
    try:
        while True:
            message = await websocket.receive_json()
            await manager.handle_messages(message, ident, id, websocket)
    except WebSocketDisconnect:
        manager.disconnect(id, websocket)
