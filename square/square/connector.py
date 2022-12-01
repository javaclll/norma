import json

import rel
import websocket


from libbaghchal import Baghchal as Bagchal

from .model import MM


def get_best_move_pgn(bagchal: Bagchal):
    alpha_object = MM()

    result = alpha_object.best_move(bagchal)
    bagchal.make_move(*result[1])

    return Bagchal.coord_to_png_unit(*result[1])


def on_message(ws, msg):

    message = json.loads(msg)

    if message["type"] == 10:
        try:
            game = Bagchal(
                turn=message["game"]["turn"],
                goat_counter=message["game"]["goat_counter"],
                goat_captured=message["game"]["goat_captured"],
                game_history=message["game"]["game_history"],
                pgn=message["game"]["pgn"],
            )
            game.set_rewards(
                t_goat_capture=7,
                t_got_trapped=-5,
                t_trap_escape=3,
                t_win=10,
                t_lose=-10,
                t_draw=-3,
                t_move=-0.25,
                g_goat_captured=-7,
                g_tiger_trap=5,
                g_tiger_escape=-3,
                g_win=10,
                g_lose=-10,
                g_draw=-3,
                g_move=-0.25,
            )
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
