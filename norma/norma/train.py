import random
from copy import deepcopy
from typing import Any, List, Optional, Tuple, TypeVar

import numpy
from libbaghchal import Baghchal, GameStatus
from livelossplot import PlotLossesKeras

from .model import tiger_model, goat_model

GOAT_EXPLORATION_FACTOR = 0.2
TIGER_EXPLORATION_FACTOR = 0.2
DISCOUNT_FACTOR = 0.50


def get_best_move(
    input_vectors,
    agent,
    exploration=True,
) -> Tuple[int, Optional[float]]:
    if agent == -1:
        inputs = numpy.asarray(input_vectors)

        if exploration:
            EXPLORATION_FACTOR = TIGER_EXPLORATION_FACTOR

            if random.uniform(0, 1) < EXPLORATION_FACTOR:
                index = random.randint(0, len(input_vectors) - 1)
                return (index, None)

        predication = tiger_model.predict_on_batch(inputs)
        max_index = predication.argmax()
        return (max_index, predication[max_index][0])

    elif agent == 1:
        inputs = numpy.asarray(input_vectors)

        if exploration:
            EXPLORATION_FACTOR = GOAT_EXPLORATION_FACTOR

            if random.uniform(0, 1) < EXPLORATION_FACTOR:
                index = random.randint(0, len(input_vectors) - 1)
                return (index, None)

        predication = goat_model.predict_on_batch(inputs)
        max_index = predication.argmax()
        return (max_index, predication[max_index][0])

    else:
        raise Exception("`agent` parameter for `get_best_move()` must be `-1` or `1`")


def reward_discounter(rewards):
    n = len(rewards)

    for (index, value) in enumerate(rewards[::-1]):
        for i in range(n - index - 1):
            rewards[n - i - 2 - index] += value * pow(1 - DISCOUNT_FACTOR, i + 1)

    return rewards


def get_or_none(alist, index):
    try:
        return alist[index]
    except:
        return None


def two_in_one_merge(items):
    merged_list = []
    for i in range(int(len(items) / 2) + 1):
        item1 = get_or_none(items, 2 * i)
        item2 = get_or_none(items, 2 * i + 1)

        if not (item1 == None and item2 == None):
            merged_list.append((item1 or 0) + (item2 or 0))

    return merged_list


def reward_transformer(rewards_g, rewards_t):
    rewards_t.pop(0)

    rewards_g = two_in_one_merge(rewards_g)
    rewards_t = two_in_one_merge(rewards_t)

    rewards_g = reward_discounter(rewards_g)
    rewards_t = reward_discounter(rewards_t)

    rewards = []

    for i in range(len(rewards_g)):
        ith_re_g = get_or_none(rewards_g, i)
        ith_re_t = get_or_none(rewards_t, i)

        if ith_re_g != None:
            rewards.append(ith_re_g)

        if ith_re_t != None:
            rewards.append(ith_re_t)

    return rewards


def play_game(exploration=True, only_record=None, record_explorations=True):
    states = []
    y_preds = []

    moves_to_exclude = []

    bagchal = Baghchal.default()
    bagchal.set_rewards(
        t_goat_capture=6.0,
        t_got_trapped=-4.0,
        t_trap_escape=3.0,
        t_win=10.0,
        t_lose=-10.0,
        t_draw=-2.5,
        t_move=-0.15,
        g_goat_captured=-6.0,
        g_tiger_trap=4.0,
        g_tiger_escape=-3.0,
        g_win=10.0,
        g_lose=-10.0,
        g_draw=-2.5,
        g_move=-0.15,
    )

    for i in range(100):
        possible_moves = bagchal.get_possible_moves()

        input_vectors = bagchal.state_as_inputs(possible_moves, mode=2, rotate_board=True)

        turn = 1 if i % 2 == 0 else -1

        best_move_index, pred_y = get_best_move(input_vectors, exploration=exploration, agent=turn)

        if pred_y or record_explorations:
            if not only_record:
                states.append(input_vectors[best_move_index])
                y_preds.append(pred_y)
            else:
                if only_record == -1 and i % 2 == 1:
                    states.append(input_vectors[best_move_index])
                    y_preds.append(pred_y)
                elif only_record == 1 and i % 2 == 0:
                    states.append(input_vectors[best_move_index])
                    y_preds.append(pred_y)
                else:
                    moves_to_exclude.append(i)
        else:
            moves_to_exclude.append(i)

        bagchal = possible_moves[best_move_index].resulting_state

        if bagchal.game_status_check().decided:
            break

    rewards = reward_transformer(
        bagchal.move_reward_goat(), bagchal.move_reward_tiger()
    )

    for superindex, index in enumerate(moves_to_exclude):
        rewards.pop(index - superindex)

    return (states, y_preds, rewards, bagchal)


def test():
    (
        states,
        y_preds,
        actual_rewards,
        bagchal,
    ) = play_game(exploration=True, only_record=1)

    print(f"{states}")
    print(f"{y_preds}")
    print(f"{actual_rewards}")
    print(f"{bagchal.pgn()}")


def training_step(exploration=True, train_on=None):
    if train_on == -1:
        model = tiger_model
    elif train_on == 1:
        model = goat_model
    else:
        raise Exception("Must provide `train_on` parameter to `training_step()`")

    (states, _, actual_rewards, bagchal,) = play_game(
        exploration=exploration,
        only_record=train_on,
    )

    positions_count = bagchal.move_count()

    game_state = bagchal.game_state()

    if game_state == GameStatus.GoatWon:
        print(f"Hello sir! GOAT WON!")
        print(f"http://localhost:3000/analysis?pgn={bagchal.pgn()}")
        game_state = 1
    elif game_state == GameStatus.TigerWon:
        game_state = -1
    else:
        print(f"Draw!!!")
        game_state = 0

    model.fit(
        states,
        actual_rewards,
        use_multiprocessing=True,
        batch_size=4,
    )

    return (game_state, positions_count, len(states))


def training_loop(model_name="magma"):
    game_counter = 0
    positions_counter = 0
    goat_trained_states = 0
    tiger_trained_states = 0

    goat_wins = 0
    tiger_wins = 0
    draws = 0

    try:
        f = open(f"weights/{model_name}/train_stats.txt", "r")

        train_stats = f.read().split(",")

        game_counter = int(train_stats[0])
        positions_counter = int(train_stats[1])
        goat_wins = int(train_stats[2])
        tiger_wins = int(train_stats[3])
        draws = int(train_stats[4])
        goat_trained_states = int(train_stats[5])
        tiger_trained_states = int(train_stats[6])

    except:
        pass

    while True:
        before_goat_wins = goat_wins
        before_tiger_wins = tiger_wins
        before_draws = draws
        before_game_counter = game_counter

        # Goat Training
        for _ in range(32):
            (won_by, played_positions, trained_positions) = training_step(
                train_on=1
            )

            if won_by == 1:
                goat_wins += 1
            elif won_by == -1:
                tiger_wins += 1
            else:
                draws += 1

            game_counter += 1
            positions_counter += played_positions
            goat_trained_states += trained_positions

        # Tiger Training
        for _ in range(32):
            (won_by, played_positions, trained_positions) = training_step(
                train_on=-1
            )

            if won_by == 1:
                goat_wins += 1
            elif won_by == -1:
                tiger_wins += 1
            else:
                draws += 1

            game_counter += 1
            positions_counter += played_positions
            tiger_trained_states += trained_positions

        f = open(f"weights/{model_name}/train_stats.txt", "w")
        f.write(
            f"{game_counter},{positions_counter},{goat_wins},{tiger_wins},{draws},{goat_trained_states},{tiger_trained_states}"
        )
        f.close()
        tiger_model.save_weights(f"weights/{model_name}/tiger")
        goat_model.save_weights(f"weights/{model_name}/goat")

        cw_goat_wins = goat_wins - before_goat_wins
        cw_tiger_wins = tiger_wins - before_tiger_wins
        cw_draws = draws - before_draws
        cw_game_counter = game_counter - before_game_counter

        print(f"---------------------------------------------------")
        print(f"OVERALL GAME STATS:")
        print(f"---------------------------------------------------")
        print(f"Goat: {goat_wins} ({((goat_wins/game_counter)*100):.2f} %)")
        print(f"Tiger: {tiger_wins} ({((tiger_wins/game_counter)*100):.2f} %)")
        print(f"Draws: {draws} ({((draws/game_counter)*100):.2f} %)")
        print(f"---------------------------------------------------")
        print(f"TRAINING STATS:")
        print(f"---------------------------------------------------")
        print(f"Games Played: {game_counter}")
        print(f"Positions Generated: {positions_counter}")
        print(f"Goat Trained States: {goat_trained_states}")
        print(f"Tiger Trained States: {tiger_trained_states}")
        print(f"Avg moves per game: {(positions_counter/game_counter):.2f}")
        print(f"---------------------------------------------------")
        print(f"CURRENT WINDOW GAME STATS:")
        print(f"---------------------------------------------------")
        print(f"Goat: {cw_goat_wins} ({((cw_goat_wins/cw_game_counter)*100):.2f} %)")
        print(f"Tiger: {cw_tiger_wins} ({((cw_tiger_wins/cw_game_counter)*100):.2f} %)")
        print(f"Draws: {cw_draws} ({((cw_draws/cw_game_counter)*100):.2f} %)")

        (_, _, _, bagchal,) = play_game(
            exploration=False,
        )

        print(f"---------------------------------------------------")
        print(f"SAMPLE GAME:")
        print(f"---------------------------------------------------")
        print(f"http://localhost:3000/analysis?pgn={bagchal.pgn()}")
        print(f"---------------------------------------------------")
