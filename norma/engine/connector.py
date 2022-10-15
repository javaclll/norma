from .constants import MODELPATH
from .model import Model
from .gamesimulation import simulate
import json
import rel
import websocket
from bagchal import Bagchal
import os
import tensorflow
import numpy as np
from random import randint, random

def loadModel():
    if os.path.exists(MODELPATH):
        savedModel = tensorflow.keras.models.load_model(MODELPATH)
    else:
        savedModel = simulate()

    return savedModel


def get_best_move_pgn(bagchal: Bagchal):

    possibleMoves = bagchal.get_possible_moves()

    savedModel = loadModel()

    predictionModel = Model(savedModel=savedModel)

    predictions = []

    for move in possibleMoves:

        source = np.zeros((5,5))

        target = np.zeros((5,5))

        target[move["move"][1][0]][move["move"][1][1]] = 1
        

        if move["move"][0] is not None:
            source[move["move"][0][0]][move["move"][0][1]] = 1
                
        # model.predict(state, action) => get reward
        predictions.append(predictionModel.predict(bagchal.board, source, target))
        # find the max reward and use that move in the gam

    bestMoveIndex = np.argmax(predictions)

    move = possibleMoves[bestMoveIndex]["resulting_state"].prev_move

    return Bagchal.coord_to_png_unit(*move)


def on_message(ws, msg):
    message = json.loads(msg)

    if message["type"] == 10:
        try:
            game = Bagchal.new()
            game.turn = message["game"]["turn"]
            game.goat_counter = message["game"]["goat_counter"]
            game.goat_captured = message["game"]["goat_captured"]
            game.game_history = message["game"]["game_history"]
            game.pgn = message["game"]["pgn"]

            pgn_unit = get_best_move_pgn(game)

            ws.send(
                json.dumps(
                    {
                        "type": 1,
                        "move": pgn_unit,
                        "game_id": message["game"]["game_id"],
                    }
                )
            )
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print(e)
            raise e


def on_error(*args, **kwargs):
    print(f"Error occured with args: {args}, {kwargs}")


def on_close(*args, **kwargs):
    print(f"Websocket closed with args: {args}, {kwargs}")


def on_open(*args, **kwargs):
    print(f"Websocket opened with args: {args}, {kwargs}")


def launch_executor():
    websocket.enableTrace(False)

    ws = websocket.WebSocketApp(
        "ws://localhost:8080/glory?ident=d4beab3f-9b3c-44df-ba62-d477fb33c67b",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(dispatcher=rel)
    rel.signal(2, rel.abort)
    rel.dispatch()
