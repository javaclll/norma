from typing import List, Optional

from fastapi import HTTPException, WebSocket, status
import random

from core.exception import ManagerException
from bagchal import Bagchal
import uuid


"""
Message Types:
    1 : Player Move Request
    2 : Player Resign Request
    3 : Load Game State
    4 : Notification Broadcast
    5 : Player Move Broadcast
    6 : Win/Loss Broadcast
    7 : Game State Broadcast
    8 : Piece Assign Notification
"""


class GameInstance:
    def __init__(
        self,
        game_id,
        tiger,
        goat,
        socket,
        game,
    ):
        self.game_id = game_id
        self.tiger = tiger
        self.goat = goat
        self.socket = socket
        self.game: Bagchal = game

    @staticmethod
    def new():
        return GameInstance(
            game_id=str(uuid.uuid4()),
            game=Bagchal.new(),
            tiger=None,
            goat=None,
            socket=[],
        )


class GameConnectionManager:
    def __init__(self):
        self.active_connections = []
        self.games: List[GameInstance] = []

    async def connect(self, websocket: WebSocket, ident: str, game_id: str):
        try:
            game = self.get_game_by_id(game_id)
        except:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Game not found!"
            )

        if game.tiger == ident:
            piece = -1
        elif game.goat == ident:
            piece = 1
        elif game.tiger == None and game.goat == None:
            piece = random.choice([-1, 1])
            if piece == -1:
                game.tiger = ident
            else:
                game.goat = ident
        elif not game.tiger:
            piece = -1
            game.tiger = ident
        elif not game.goat:
            piece = 1
            game.goat = ident
        else:
            piece = 0

        await websocket.accept()

        game.socket.append(websocket)

        message = {
            "type": 8,
            "piece": piece,
        }

        await websocket.send_json(message)

    def disconnect(self, ident):
        for cons in self.active_connections:
            if cons["ident"] == ident:
                self.active_connections.remove(cons)
                return

    def create_game(
        self,
    ):
        game = GameInstance.new()
        self.games.append(game)

        return game.game_id

    async def broadcast(self, game_id, message):
        game = self.get_game_by_id(game_id)

        for conn in game.socket:  # type: ignore
            await conn.send_json(message)

    async def handle_messages(self, message, ident, game_id, ws: WebSocket):
        message_type = message["type"]

        if message_type == 1:
            try:
                move_result = await self.make_move(game_id, ident, message["move"])

                message = {"type": 5, "move": message["move"]}
                await self.broadcast(game_id, message)

                if move_result["decided"]:
                    message = {
                        "type": 6,
                        "won_by": move_result["won_by"],
                        "reason": "normal",
                    }
                    await self.broadcast(game_id, message)

            except ManagerException as e:
                message = {"type": 4, "message": e.message}
                await ws.send_json(message)

        elif message_type == 2:
            try:
                won_by = await self.resign(game_id, ident)

                message = {"type": 6, "won_by": won_by}
                await self.broadcast(game_id, message)

            except ManagerException as e:
                message = {"type": 4, "message": e.message}
                await ws.send_json(message)

        elif message_type == 3:
            try:
                await self.load_game(game_id, message["pgn"])  # type: ignore

                message = {"type": 7, "pgn": message["pgn"]}
                await self.broadcast(game_id, message)
            except ManagerException as e:
                message = {"type": 4, "message": e.message}
                await ws.send_json(message)

    def get_game_by_id(self, game_id):
        for game in self.games:
            if game.game_id == game_id:
                return game

        raise ManagerException(
            message="Failed to find the game with mathing game_id and ident!"
        )

    async def make_move(self, game_id, ident, move):
        game_instance: Optional[GameInstance] = self.get_game_by_id(game_id)

        if game_instance.tiger == ident:
            ident_piece = -1
        elif game_instance.goat == ident:
            ident_piece = 1
        else:
            raise ManagerException(message="Unauthorized user!")

        if ident_piece != game_instance.game.turn:
            raise ManagerException(message="Not the player's turn!")

        source, destination = Bagchal.pgn_unit_to_coord(move)

        game_instance.game.move(source, destination)

        game_status = game_instance.game.game_status_check()

        if game_status["decided"]:
            return {"decided": True, "won_by": game_status["won_by"]}

        return {"decided": False}

    def load_game(self, game_id, pgn):
        game_instance = self.get_game_by_id(game_id)

        game_instance.game.load_game(pgn)

    async def resign(self, game_id, ident):
        game_instance: Optional[GameInstance] = self.get_game_by_id(game_id)

        if game_instance.goat == ident:
            resign_resp = game_instance.game.resign(1)
        elif game_instance.tiger == ident:
            resign_resp = game_instance.game.resign(-1)
        else:
            raise ManagerException(message="Unauthorized user!")

        return resign_resp["won_by"]

    def evict_game(self, game_id):
        for game in self.games:
            if game.game_id == game_id:
                self.games.remove(game)
                break

    def assign_game(self, game_id, ident, piece):
        for game in self.games:
            if game.game_id == game_id:
                if piece == -1:
                    game.tiger = ident
                else:
                    game.goat = ident
                break


manager = GameConnectionManager()
