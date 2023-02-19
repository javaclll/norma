from .tiger_model import (
    tiger_actor_model,
    tiger_critic_model,
    tiger_optimizer,
    tiger_actor_loss,
    tiger_critic_loss,
)

from .goat_model import (
    goat_actor_model,
    goat_critic_model,
    placement_actor_model,
    placement_critic_model,
    goat_optimizer,
    goat_actor_loss,
    goat_critic_loss,
)

import libbaghchal
import tensorflow as tf
import numpy as np
import random

from .stats import Stats
from typing import Tuple, List


def get_move(vectors: List, model: tf.keras.Model):
    pred = model.predict(np.array([vectors], dtype=np.int8))
    action = np.random.choice(np.arange(pred.size), p=pred[0])

    return (action, pred)


def play_game():
    states = []
    preds = []

    bagchal = libbaghchal.Baghchal.default()

    bagchal.set_rewards(
        t_goat_capture=6.0,
        t_got_trapped=-4.0,
        t_trap_escape=3.0,
        t_win=10.0,
        t_lose=-10.0,
        t_draw=-2.5,
        t_move=-0.15,
        g_goat_captured=-6.0,
        g_tiger_trap=6.0,
        g_tiger_escape=-3.0,
        g_win=10.0,
        g_lose=-10.0,
        g_draw=-2.5,
        g_move=-0.15,
    )

    for _ in range(100):
        if bagchal.turn() == -1:
            model = tiger_actor_model
            i2m = libbaghchal.Baghchal.i2m_tiger
        elif bagchal.turn() == 1 and bagchal.goat_counter() < 20:
            model = placement_actor_model
            i2m = libbaghchal.Baghchal.i2m_placement
        else:
            model = goat_actor_model
            i2m = libbaghchal.Baghchal.i2m_goat

        input_vector = bagchal.state_as_input_actor(None, mode=6, rotate_board=True)

        index, pred = get_move(vectors=input_vector, model=model)

        source, destination = i2m(index)

        states.append(bagchal.index_to_input(index))
        preds.append(pred)

        bagchal.make_move(source=source, target=destination, eval_res=None)

        if bagchal.game_status_check().decided:
            break


def training_step(train_on: int) -> Tuple[int, int, int, int, int, int]:
    play_game()


def training_loop(model_name="new_model"):
    stats = Stats(model_name)

    while True:
        (
            played_positions,
            trained_positions,
            t_games,
            t_goat_wons,
            t_tiger_wons,
            t_draws,
        ) = training_step(train_on=1)

        stats.add(
            game_counter=t_games,
            positions_counter=played_positions,
            goat_wins=t_goat_wons,
            tiger_wins=t_tiger_wons,
            draws=t_draws,
            goat_trained_states=trained_positions,
            tiger_trained_states=0,
            loss=1,
        )

        # Tiger Training
        for _ in range(1):
            (
                played_positions,
                trained_positions,
                t_games,
                t_goat_wons,
                t_tiger_wons,
                t_draws,
            ) = training_step(train_on=-1)

            stats.add(
                game_counter=t_games,
                positions_counter=played_positions,
                goat_wins=t_goat_wons,
                tiger_wins=t_tiger_wons,
                draws=t_draws,
                tiger_trained_states=trained_positions,
                goat_trained_states=0,
                loss=1,
            )

        goat_actor_model.save_weights(f"weights/{model_name}/goat_actor")
        goat_critic_model.save_weights(f"weights/{model_name}/goat_critic")
        tiger_actor_model.save_weights(f"weights/{model_name}/tiger_actor")
        tiger_critic_model.save_weights(f"weights/{model_name}/tiger_critic")
        placement_critic_model.save_weights(f"weights/{model_name}/placement_actor")
        placement_actor_model.save_weights(f"weights/{model_name}/placement_critic")
