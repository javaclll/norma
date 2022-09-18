import _thread
import json
import time

import rel
import websocket
from bagchal import Bagchal
from model import get_best_move

"""
bagchal = Bagchal.new()


possible_moves = bagchal.get_possible_moves()

bagchal = possible_moves[0]["resulting_state"]


while bagchal.game_status_check()["decided"] != True:
    try:
        print(f"Currently on move: {len(bagchal.game_history)}")
        possible_moves = bagchal.get_possible_moves()

        input_vectors = bagchal.state_as_inputs(possible_moves)

        best_move = get_best_move(input_vectors)

        bagchal = possible_moves[best_move]["resulting_state"]

    except Exception as e:
        print(f"Possible Moves: {bagchal.get_possible_moves()}")
        print(f"Possible Moves: {bagchal.game_status_check()}")
        print(bagchal.turn)
        print(bagchal.board)
        raise e

print(bagchal.pgn)
"""


def get_best_move_pgn(bagchal: Bagchal):
    possible_moves = bagchal.get_possible_moves()

    input_vectors = bagchal.state_as_inputs(possible_moves)

    best_move = get_best_move(input_vectors)

    move = possible_moves[best_move]["resulting_state"].prev_move

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
            print(e)
            raise e


def on_error(*args, **kwargs):
    pass


def on_close(*args, **kwargs):
    print("Websocket closed!")


def on_open(*args, **kwargs):
    print("Websocket opened!")


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        "ws://localhost:8080/glory?ident=d4beab3f-9b3c-44df-ba62-d477fb33c67b",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
