import json
import random
import uuid
from typing import List, Optional

from bagchal import Bagchal
from fastapi import HTTPException, WebSocket, status

from core.exception import ManagerException
from core.redis import redis_client

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
    9 : Request Piece Assign Notification
"""


class GameInstance:
    def __init__(
        self,
        game_id,
        tiger,
        goat,
        socket,
        game,
        pgn,
    ):
        self.game_id = game_id
        self.tiger = tiger
        self.goat = goat
        self.socket = socket
        self.game: Bagchal = game
        self.pgn = pgn

    @staticmethod
    def new():
        return GameInstance(
            game_id=str(uuid.uuid4()),
            game=Bagchal.new(),
            tiger=None,
            goat=None,
            socket=[],
            pgn="",
        )


class GameConnectionManager:
    def __init__(self):
        self.active_connections = []
        self.games: List[GameInstance] = []

        self.load_from_redis()

    def save_to_redis(self):
        save_games = []

        for game_instance in self.games:
            save_games.append(
                {
                    "game_id": game_instance.game_id,
                    "tiger": game_instance.tiger,
                    "goat": game_instance.goat,
                    "turn": game_instance.game.turn,
                    "goat_counter": game_instance.game.goat_counter,
                    "goat_captured": game_instance.game.goat_captured,
                    "game_state": game_instance.game.game_state,
                    "game_history": game_instance.game.game_history,
                    "pgn": game_instance.pgn,
                }
            )

        if len(save_games) != 0:
            redis_client.set("games", json.dumps(save_games))

    def load_from_redis(self):
        games = redis_client.get("games")

        if not games:
            return

        games = json.loads(games)

        for game in games:
            self.games.append(
                GameInstance(
                    game_id=game.get("game_id"),
                    tiger=game.get("tiger"),
                    goat=game.get("goat"),
                    socket=[],
                    pgn=game.get("pgn"),
                    game=Bagchal(
                        turn=game.get("turn"),
                        goat_counter=game.get("goat_counter"),
                        goat_captured=game.get("goat_captured"),
                        game_state=game.get("game_state"),
                        game_history=game.get("game_history"),
                    ),
                )
            )

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

        message = {
            "type": 7,
            "pgn": game.pgn,
            "turn": game.game.turn,
            "captured_goats": game.game.goat_captured,
            "placed_goats": game.game.goat_counter,
            "history": game.game.game_history,
        }

        await websocket.send_json(message)

    def disconnect(self, id, socket):
        game = self.get_game_by_id(id)

        game.socket.remove(socket)

    def create_game(
        self,
    ):
        game = GameInstance.new()
        self.games.append(game)

        self.save_to_redis()

        return game.game_id

    async def broadcast(self, game_id, message):
        game = self.get_game_by_id(game_id)

        for conn in game.socket:  # type: ignore
            await conn.send_json(message)

    async def handle_messages(self, message, ident, game_id, ws: WebSocket):
        message_type = message["type"]

        if message_type == 1:
            try:
                move_result = await self.make_move(
                    game_id, ident, message["move"].replace(" ", "")
                )

                self.save_to_redis()

                game = move_result["game"]

                message = {
                    "type": 7,
                    "pgn": game.pgn,
                    "turn": game.game.turn,
                    "captured_goats": game.game.goat_captured,
                    "placed_goats": game.game.goat_counter,
                    "history": game.game.game_history,
                }
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

                self.save_to_redis()

                message = {"type": 6, "won_by": won_by}
                await self.broadcast(game_id, message)

            except ManagerException as e:
                message = {"type": 4, "message": e.message}
                await ws.send_json(message)

        elif message_type == 3:
            try:
                await self.load_game(game_id, message["pgn"])  # type: ignore

                self.save_to_redis()

                message = {"type": 7, "pgn": message["pgn"]}
                await self.broadcast(game_id, message)
            except ManagerException as e:
                message = {"type": 4, "message": e.message}
                await ws.send_json(message)

        elif message_type == 9:
            game_instance: Optional[GameInstance] = self.get_game_by_id(game_id)

            if game_instance.tiger == ident:
                ident_piece = -1
            elif game_instance.goat == ident:
                ident_piece = 1
            else:
                ident_piece = 0

            message = {
                "type": 8,
                "piece": ident_piece,
            }

            await ws.send_json(message)

    def get_game_by_id(self, game_id):
        for game in self.games:
            if game.game_id == game_id:
                return game

        raise ManagerException(
            message="Failed to find the game with mathing game_id and ident!"
        )

    async def make_move(self, game_id, ident, move: str):
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

        if not game_instance.pgn or game_instance.pgn == "":
            game_instance.pgn = move
        else:
            game_instance.pgn = game_instance.pgn + "-" + move

        if game_status["decided"]:
            return {"decided": True, "won_by": game_status["won_by"]}

        return {"decided": False, "game": game_instance}

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

        self.save_to_redis()

    def assign_game(self, game_id, ident, piece):
        for game in self.games:
            if game.game_id == game_id:
                if piece == -1:
                    game.tiger = ident
                else:
                    game.goat = ident
                break

        self.save_to_redis()


manager = GameConnectionManager()
