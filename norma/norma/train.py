from libbaghchal import Baghchal, GameStatus
from .model import model
import numpy
import random
from typing import List, Tuple, List, Any, Optional, TypeVar
from livelossplot import PlotLossesKeras
from copy import deepcopy

GOAT_EXPLORATION_FACTOR = 0.2
TIGER_EXPLORATION_FACTOR = 0.2
DISCOUNT_FACTOR = 0.50


def get_best_move(input_vectors, exploration=True) -> Tuple[int, Optional[float]]:
    inputs = numpy.asarray(input_vectors)

    if exploration:
        # FIXME: Position of turn in vector is not at the end
        if input_vectors[0][-1] == 1:
            EXPLORATION_FACTOR = TIGER_EXPLORATION_FACTOR
        else:
            EXPLORATION_FACTOR = GOAT_EXPLORATION_FACTOR

        if random.uniform(0, 1) < EXPLORATION_FACTOR:
            index = random.randint(0, len(input_vectors) - 1)
            return (index, None)

    predication = model.predict_on_batch(inputs)
    max_index = predication.argmax()
    return (max_index, predication[max_index][0])


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


def test():
    goat = [0, 0, 2, 0, -4, 8]
    tiger = [0, 1, 2, -2, 0, -8]

    # tiger.pop(0)
    #
    # rewards_g = two_in_one_merge(goat)
    # rewards_t = two_in_one_merge(tiger)
    #
    # print(f"Goat: {rewards_g}")
    # print(f"Tiger: {rewards_t}")
    #
    #
    # rewards_g = reward_discounter(rewards_g)
    # rewards_t = reward_discounter(rewards_t)
    #
    # print(f"Goat: {rewards_g}")
    # print(f"Tiger: {rewards_t}")

    print(f"Transformed: {reward_transformer(deepcopy(goat), deepcopy(tiger))}")
    # tiger.pop(0)
    # print(f"Goat: {reward_discounter(goat)}")
    # print(f"Tiger: {reward_discounter(tiger)}")


def play_game(exploration=True):
    states = []
    y_preds = []

    exploration_moves = []

    bagchal = Baghchal.default()
    bagchal.set_rewards(
        t_goat_capture=2.0,
        t_got_trapped=-1.0,
        t_trap_escape=0.5,
        t_win=5.0,
        t_lose=-5.0,
        t_draw=-3.0,
        t_move=-0.15,
        g_goat_captured=-7.0,
        g_tiger_trap=3.0,
        g_tiger_escape=-3.0,
        g_win=10.0,
        g_lose=-10.0,
        g_draw=-0.5,
        g_move=-0.15,
    )

    for i in range(100):
        # while not bagchal.game_status_check().decided:
        possible_moves = bagchal.get_possible_moves()

        input_vectors = bagchal.state_as_inputs(possible_moves)

        best_move_index, pred_y = get_best_move(input_vectors, exploration)

        if pred_y:
            states.append(input_vectors[best_move_index])
            y_preds.append(pred_y)
        else:
            exploration_moves.append(i)

        bagchal = possible_moves[best_move_index].resulting_state

        if bagchal.game_status_check().decided:
            break

    rewards = reward_transformer(
        bagchal.move_reward_goat(), bagchal.move_reward_tiger()
    )

    for superindex, index in enumerate(exploration_moves):
        rewards.pop(index - superindex)

    return (states, y_preds, rewards, bagchal)


def training_loop():
    game_counter = 0
    positions_counter = 0

    goat_wins = 0
    tiger_wins = 0
    draws = 0

    try:
        f = open("weights/train_stats.txt", "r")

        train_stats = f.read().split(",")

        game_counter = int(train_stats[0])
        positions_counter = int(train_stats[1])
        goat_wins = int(train_stats[2])
        tiger_wins = int(train_stats[3])
        draws = int(train_stats[4])

    except:
        pass

    while True:
        (
            states,
            y_preds,
            actual_rewards,
            bagchal,
        ) = play_game(exploration=game_counter % 20 != 0)

        # new_state = states[::2]
        # new_actual_rewards = states[::2]

        positions_count = bagchal.move_count()

        game_state = bagchal.game_state()

        if game_state == GameStatus.GoatWon:
            print(f"Hello sir! GOAT WON!")
            print(f"http://localhost:3000/analysis?pgn={bagchal.pgn()}")
            goat_wins += 1
        elif game_state == GameStatus.TigerWon:
            tiger_wins += 1
        else:
            print(f"Draw!!!")
            draws += 1

        # model.fit(
        #     new_state,
        #     new_actual_rewards,
        #     use_multiprocessing=True,
        #     batch_size=4,
        # )

        model.fit(
            states,
            actual_rewards,
            use_multiprocessing=True,
            batch_size=4,
        )

        game_counter += 1
        positions_counter += positions_count

        if game_counter % 20 == 0:
            f = open("weights/train_stats.txt", "w")
            f.write(
                f"{game_counter},{positions_counter},{goat_wins},{tiger_wins},{draws}"
            )
            f.close()
            model.save_weights("weights/magma")

            print(f"{y_preds}")
            print(f"http://localhost:3000/analysis?pgn={bagchal.pgn()}")
            print(f"Goat: {goat_wins} ({((goat_wins/game_counter )*100):.2f} %)")
            print(f"Tiger: {tiger_wins} ({((tiger_wins/game_counter )*100):.2f} %)")
            print(f"Draws: {draws} ({( (draws/game_counter )*100):.2f} %)")
            print(f"Stats for this session:")
            print(f"Games Played: {game_counter}")
            print(f"Positions: {positions_counter}")
            print(f"Avg moves per game: {positions_counter/game_counter}")
