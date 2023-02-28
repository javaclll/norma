import random
from typing import List, Tuple

import libbaghchal
import numpy as np
import tensorflow as tf

from .goat_model import (
    goat_actor_model,
    goat_critic_model,
    placement_actor_model,
    placement_critic_model,
)
from .reward import reward_transformer
from .stats import Stats
from .tiger_model import tiger_actor_model, tiger_critic_model


def get_move(vectors: List, model: tf.keras.Model) -> Tuple[int, List, int]:
    symmetry_chosen = np.random.random_integers(0, 6)
    pred = model.predict(np.array(vectors, dtype=np.int8))
    action = np.random.choice(np.arange(pred[0].size), p=pred[symmetry_chosen])

    return (action, pred, symmetry_chosen)


def play_game() -> Tuple[List, List, int]:
    states = []
    preds = []
    won_by = 0

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

        index, pred, symmetry_choosen = get_move(vectors=input_vector, model=model)

        source, destination = i2m(index)

        states.append(bagchal.index_to_input(index, symmetry=symmetry_choosen))
        preds.append(pred)

        bagchal.make_move_with_symmetry(
            source=source, target=destination, symmetry=symmetry_choosen
        )

        game_status = bagchal.game_status_check()
        if game_status.decided:
            won_by = game_status.won_by
            break

    rewards = reward_transformer(
        bagchal.move_reward_goat(), bagchal.move_reward_tiger(), states, y_preds
    )

    sar_pair = list(zip(states, rewards))
    random.shuffle(sar_pair)

    return (sar_pair, preds, won_by)


def training_step(train_on: int) -> Tuple[int, int, int, int, int, int]:  # type: ignore
    played_positions = 0
    trained_positions = 0
    t_games = 0
    t_goat_wons = 0
    t_tiger_wons = 0
    t_draws = 0

    for _ in range(50):
        (states, preds, won_by) = play_game()
        print("Hello")

        played_positions += len(states) * 7
        t_games += 1
        if won_by == 1:
            t_goat_wons += 1
        elif won_by == -1:
            t_tiger_wons += 1
        else:
            t_draws += 1

    trained_positions = played_positions

    return (
        played_positions,
        trained_positions,
        t_games,
        t_goat_wons,
        t_tiger_wons,
        t_draws,
    )


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
