from helpers import movestoAction
from constants import GOATMODELPATH, MODELPATH, TARGETMODELPATH, TIGERMODELPATH
from model import Model
from gamesimulation import Simulator
import json
import rel
import websocket
from libbaghchal import Baghchal
import os
import numpy as np
import math
import tensorflow

def loadModel(path):
    if os.path.exists(path):
        savedModel = tensorflow.keras.models.load_model(path)
    else:
        simulator = Simulator()
        simulator.simulate()
        savedModel = simulator.targetModel.model
    print(path)
    print("Model Loaded")
    return savedModel

def get_best_move_pgn(bagchal: Baghchal):

    possibleMoves = bagchal.get_possible_moves()

    if bagchal.turn() == 1:
        savedModel = loadModel(GOATMODELPATH)
    else:
        savedModel = loadModel(TIGERMODELPATH)

    predictionModel = Model(savedModel=savedModel)

    actions = []
       
    prediction = predictionModel.predict(bagchal)[0]

    action = np.argmax(prediction)

    for move in possibleMoves:
        actions.append(movestoAction(move.move[0], move.move[1]))
            
    while action not in actions:
        prediction[action] = - math.inf
        action = np.argmax(prediction)

    moveIndex = actions.index(action)
            
    move = possibleMoves[moveIndex].resulting_state.prev_move()
    print(move)
    return Baghchal.coord_to_png_unit(*(move[::-1]))


def on_message(ws, msg):
    message = json.loads(msg)

    if message["type"] == 10:
        try:
            game = Baghchal(turn= message["game"]["turn"], goat_counter= message["game"]["goat_counter"], goat_captured= message["game"]["goat_captured"], game_history= message["game"]["game_history"], pgn= message["game"]["pgn"])
            # game.turn = message["game"]["turn"]
            # game.goat_counter = message["game"]["goat_counter"]
            # game.goat_captured = message["game"]["goat_captured"]
            # game.game_history = message["game"]["game_history"]
            # game.pgn = message["game"]["pgn"]

            pgn_unit = get_best_move_pgn(game)
            print(pgn_unit)
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
