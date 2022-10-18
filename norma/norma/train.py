from libbaghchal import Baghchal, GameStatus
from tensorflow.python.eager.context import device_policy
from .model import model
import numpy
import random
from typing import List, Tuple, List, Any, Optional, TypeVar


EXPLORATION_FACTOR = 0.5
DISCOUNT_FACTOR = 0.20


def get_best_move(input_vectors) -> Tuple[int, Optional[float]]:
    inputs = numpy.asarray(input_vectors)

    if random.uniform(0, 1) < EXPLORATION_FACTOR:
        index = random.randint(0, len(input_vectors) - 1)
        return (index, None)
    else:
        predication = model.predict_on_batch(inputs)
        max_index = predication.argmax()
        return (max_index, predication[max_index][0])


def reward_discounter(rewards):
    n = len(rewards)

    for (index, value) in enumerate(rewards[::-1]):
        for i in range(n - index - 1):
            rewards[n - i - 2 - index] += value * pow(DISCOUNT_FACTOR, i + 1)

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
    rewards_g = reward_discounter(rewards_g)
    rewards_t = reward_discounter(rewards_t)

    rewards_t.pop(0)

    rewards_g = two_in_one_merge(rewards_g)
    rewards_t = two_in_one_merge(rewards_t)

    rewards = []

    for i in range(len(rewards_g)):
        ith_re_g = get_or_none(rewards_g, i)
        ith_re_t = get_or_none(rewards_t, i)

        if ith_re_g != None:
            rewards.append(ith_re_g)

        if ith_re_t != None:
            rewards.append(ith_re_t)

    return rewards


def play_a_complete_game():
    states = []
    y_preds = []

    bagchal = Baghchal.default()

    while not bagchal.game_status_check().decided:
        try:
            possible_moves = bagchal.get_possible_moves()

            input_vectors = bagchal.state_as_inputs(possible_moves)

            best_move_index, pred_y = get_best_move(input_vectors)

            states.append(input_vectors[best_move_index])
            y_preds.append(pred_y)

            bagchal = possible_moves[best_move_index].resulting_state

        except Exception as e:
            # print(f"Possible Moves: {bagchal.get_possible_moves()}")
            # print(f"Possible Moves: {bagchal.game_status_check()}")
            # print(bagchal.turn)
            # print(bagchal.board)
            raise e

    rewards = reward_transformer(
        bagchal.move_reward_goat(), bagchal.move_reward_tiger()
    )
    print(f"{bagchal.pgn()}")

    # print(f"States: {states}")
    #
    # print(bagchal.pgn())
    # print(bagchal.move_reward_goat())
    # print(bagchal.move_reward_tiger())

    if bagchal.game_state == GameStatus.GoatWon:
        print("Goat Won")
    else:
        print("Tiger Won")

    return (states, y_preds, rewards)


def training_loop():
    while True:
        (states, y_preds, actual_rewards) = play_a_complete_game()
        print(f"{actual_rewards}")
        # model.fit(states, g_rewards)
        break


#
#
# # state, action, result
# # true
# # Reward must go back
