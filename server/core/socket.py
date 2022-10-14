import json
import random
import uuid
from typing import List, Optional

from bagchal import Bagchal
from fastapi import HTTPException, WebSocket, status

from core import settings
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
    10 : Request next move from norma
"""


class GameInstance:
    def __init__(
        self,
        game_id,
        tiger,
        goat,
        socket,
        game,
        is_with_norma,
    ):
        self.game_id = game_id
        self.tiger = tiger
        self.goat = goat
        self.socket = socket
        self.game: Bagchal = game
        self.is_with_norma = is_with_norma

    @staticmethod
    def new():
        return GameInstance(
            game_id=str(uuid.uuid4()),
            game=Bagchal.new(),
            tiger=None,
            goat=None,
            socket=[],
            is_with_norma=False,
        )


class GameConnectionManager:
    def __init__(self):
        self.norma_executors = []
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
                    "prev_move": game_instance.game.prev_move,
                    "turn": game_instance.game.turn,
                    "goat_counter": game_instance.game.goat_counter,
                    "goat_captured": game_instance.game.goat_captured,
                    "game_state": game_instance.game.game_state,
                    "game_history": game_instance.game.game_history,
                    "pgn": game_instance.game.pgn,
                    "is_with_norma": game_instance.is_with_norma,
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
                    game=Bagchal(
                        turn=game.get("turn"),
                        goat_counter=game.get("goat_counter"),
                        goat_captured=game.get("goat_captured"),
                        game_state=game.get("game_state"),
                        game_history=game.get("game_history"),
                        pgn=game.get("pgn"),
                        prev_move=game.get("prev_move"),
                    ),
                    is_with_norma=game.get("is_with_norma"),
                )
            )

    async def executor_connect(self, websocket: WebSocket, ident: str):
        if ident != settings.ENGINE_IDENT:
            return

        await websocket.accept()

        wants_norma = await self.get_wants_norma()

        for game_id in wants_norma:
            game_instance = self.get_game_by_id(game_id)
            message = {
                "type": 10,
                "game": {
                    "game_id": game_instance.game_id,
                    "turn": game_instance.game.turn,
                    "goat_counter": game_instance.game.goat_counter,
                    "goat_captured": game_instance.game.goat_captured,
                    "game_history": game_instance.game.game_history,
                    "pgn": game_instance.game.pgn,
                },
            }
            await websocket.send_json(message)

        self.norma_executors.append(websocket)

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
            "pgn": game.game.pgn,
            "turn": game.game.turn,
            "captured_goats": game.game.goat_captured,
            "placed_goats": game.game.goat_counter,
            "history": game.game.game_history,
        }

        await websocket.send_json(message)

    def disconnect(self, id, socket):
        game = self.get_game_by_id(id)

        game.socket.remove(socket)

    def executor_disconnect(self, socket):
        self.norma_executors.remove(socket)

    def create_game(self, with_norma=False):
        game = GameInstance.new()

        if with_norma:
            game.is_with_norma = True

        self.games.append(game)

        self.save_to_redis()

        return game.game_id

    async def broadcast(self, game_id, message):
        game = self.get_game_by_id(game_id)

        for conn in game.socket:  # type: ignore
            await conn.send_json(message)

    async def handle_norma_messages(self, message, ident, ws: WebSocket):
        message_type = message["type"]

        game_id = message["game_id"]

        if message_type == 1:
            try:
                move_result = await self.make_move(
                    game_id, ident, message["move"].replace(" ", "")
                )

                self.save_to_redis()

                game = move_result["game"]

                message = {
                    "type": 7,
                    "pgn": game.game.pgn,
                    "turn": game.game.turn,
                    "captured_goats": game.game.goat_captured,
                    "placed_goats": game.game.goat_counter,
                    "history": game.game.game_history,
                }

                wants_norma = json.loads(redis_client.get("wants_norma"))  # type: ignore

                wants_norma.remove(game_id)

                redis_client.set("wants_norma", json.dumps(wants_norma))

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
                    "pgn": game.game.pgn,
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

    async def assign_game_to_engine(self, game_id, ident, piece):
        self.assign_game(game_id, ident, piece)
        norma_game_list = redis_client.get("norma_associated_games")

        if norma_game_list:
            norma_game_list = json.loads(norma_game_list)
        else:
            norma_game_list = []

        if piece == 1:
            await self.append_to_wants_norma(game_id)
            await self.inform_executors(game_id=game_id)

        norma_game_list.append(
            {
                "id": game_id,
                "piece": piece,
            }
        )

        redis_client.set("norma_associated_games", json.dumps(norma_game_list))

    async def append_to_wants_norma(self, game_id):
        wants_norma = await self.get_wants_norma()

        wants_norma.append(game_id)

        redis_client.set("wants_norma", json.dumps(wants_norma))

    async def get_wants_norma(self):
        wants_norma = redis_client.get("wants_norma")

        if wants_norma:
            return json.loads(wants_norma)
        else:
            return []

    async def inform_executors(self, game_id=None, game_instance=None):
        if game_id:
            game: GameInstance = self.get_game_by_id(game_id)
        else:
            game: GameInstance = game_instance  # type: ignore

        if len(self.norma_executors) != 0:
            message = {
                "type": 10,
                "game": {
                    "game_id": game.game_id,
                    "turn": game.game.turn,
                    "goat_counter": game.game.goat_counter,
                    "goat_captured": game.game.goat_captured,
                    "game_history": game.game.game_history,
                    "pgn": game.game.pgn,
                },
            }
            await random.choice(self.norma_executors).send_json(message)

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

        if game_status["decided"]:
            return {
                "decided": True,
                "won_by": game_status["won_by"],
                "game": game_instance,
            }

        if game_instance.is_with_norma and ident != settings.ENGINE_IDENT:
            await self.append_to_wants_norma(game_id)
            await self.inform_executors(game_instance=game_instance)

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