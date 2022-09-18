import random
from typing import Any, Optional

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from core.config import settings

from core.ident import Ident, get_ident
from core.socket import manager

router = APIRouter()


@router.post("/create-game")
async def create_game(
    ident: Ident = Depends(get_ident),
    preference: Optional[int] = None,  # -1 for Tiger and 1 for Goat
    with_norma: Optional[bool] = False,
) -> Any:
    if preference in [-1, 1]:
        piece = preference
    else:
        piece = random.choice([-1, 1])

    if with_norma:
        pass

    game_id = manager.create_game(with_norma=with_norma)

    manager.assign_game(game_id, ident.value, piece)

    if with_norma:
        manager.assign_game_to_engine(
            game_id, settings.ENGINE_IDENT, -1 if piece == 1 else 1
        )

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
async def glory(
    websocket: WebSocket,
    ident: str,
) -> Any:
    await manager.executor_connect(websocket, ident)
    try:
        while True:
            message = await websocket.receive_json()
            await manager.handle_norma_messages(message, ident, websocket)
    except WebSocketDisconnect:
        manager.executor_disconnect(websocket)
