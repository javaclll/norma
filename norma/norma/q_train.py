import random
from typing import Optional, Tuple

import libbaghchal
import numpy

from .model import goat_model, tiger_model

GOAT_EXPLORATION_FACTOR = 0.15
TIGER_EXPLORATION_FACTOR = 0.15
DISCOUNT_FACTOR = 0.90
TDN = 2
SAMPLE_RATE = 0.90


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


def get_or_zero(alist, index):
    try:
        return alist[index]
    except:
        return 0


def two_in_one_merge(items):
    merged_list = []
    for i in range(int(len(items) / 2) + 1):
        item1 = get_or_none(items, 2 * i)
        item2 = get_or_none(items, 2 * i + 1)

        if not (item1 == None and item2 == None):
            merged_list.append((item1 or 0) + (item2 or 0))

    return merged_list


def td_reward_transformer(rewards_g, rewards_t, states, y_preds, rotate_board=True):
    rewards_t.pop(0)

    rewards_g = two_in_one_merge(rewards_g)
    rewards_t = two_in_one_merge(rewards_t)

    for index in range(len(rewards_g)):
        beyond_first = 0

        for i in range(TDN - 1):
            beyond_first += get_or_zero(rewards_g, index + i + 1) * pow(
                DISCOUNT_FACTOR, i + 1
            )

        rest_predicted = y_preds[2 * index]

        if not rest_predicted:
            rest_predicted = goat_model.predict([states[2 * index]], verbose=0)[0][0]  # type: ignore

        rewards_g[index] += beyond_first + rest_predicted * pow(DISCOUNT_FACTOR, TDN)

    for index in range(len(rewards_t)):
        beyond_first = 0

        for i in range(TDN - 1):
            beyond_first += get_or_zero(rewards_t, index + i + 1) * pow(
                DISCOUNT_FACTOR, i + 1
            )

        rest_predicted = y_preds[2 * index + 1]

        if not rest_predicted:
            rest_predicted = tiger_model.predict([states[2 * index + 1]], verbose=0)[0][0]  # type: ignore

        rewards_t[index] += beyond_first + rest_predicted * pow(DISCOUNT_FACTOR, TDN)

    rewards = []

    for i in range(len(rewards_g)):
        ith_re_g = get_or_none(rewards_g, i)
        ith_re_t = get_or_none(rewards_t, i)

        if ith_re_g != None:
            rewards.append(ith_re_g)

        if ith_re_t != None:
            rewards.append(ith_re_t)

    if rotate_board:
        return [x for x in rewards for _ in range(7)]
    else:
        return rewards


def reward_transformer(rewards_g, rewards_t, rotate_board=True):
    rewards_t.pop(0)

    rewards_g = two_in_one_merge(rewards_g)
    rewards_t = two_in_one_merge(rewards_t)

    for index in range(len(rewards_g)):
        beyond_first = 0

        for i in range(len(rewards_g)):
            beyond_first += get_or_zero(rewards_g, index + i + 1) * pow(
                DISCOUNT_FACTOR, i + 1
            )

        rewards_g[index] += beyond_first

    for index in range(len(rewards_t)):
        beyond_first = 0

        for i in range(len(rewards_t)):
            beyond_first += get_or_zero(rewards_t, index + i + 1) * pow(
                DISCOUNT_FACTOR, i + 1
            )

        rewards_t[index] += beyond_first

    rewards = []

    for i in range(len(rewards_g)):
        ith_re_g = get_or_none(rewards_g, i)
        ith_re_t = get_or_none(rewards_t, i)

        if ith_re_g != None:
            rewards.append(ith_re_g)

        if ith_re_t != None:
            rewards.append(ith_re_t)

    if rotate_board:
        return [x for x in rewards for _ in range(7)]
    else:
        return rewards


def play_game(
    exploration=True, only_record=None, record_explorations=False, rotate_board=True
):
    states = []
    y_preds = []

    moves_to_exclude = []

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

    # bagchal.set_rewards(
    #     t_goat_capture=6.0,
    #     t_got_trapped=0.0,
    #     t_trap_escape=0.0,
    #     t_win=10.0,
    #     t_lose=-10.0,
    #     t_draw=-2.5,
    #     t_move=-0.15,
    #     g_goat_captured=-6.0,
    #     g_tiger_trap=6.0,
    #     g_tiger_escape=-3.0,
    #     g_win=10.0,
    #     g_lose=-10.0,
    #     g_draw=-1.5,
    #     g_move=-0.15,
    # )

    # bagchal.set_rewards(
    #     t_goat_capture=10.0,
    #     t_got_trapped=0,
    #     t_trap_escape=0,
    #     t_win=0,
    #     t_lose=0,
    #     t_draw=0,
    #     t_move=0,
    #     g_goat_captured=0,
    #     g_tiger_trap=0,
    #     g_tiger_escape=0,
    #     g_win=0,
    #     g_lose=0,
    #     g_draw=0,
    #     g_move=0,
    # )

    for i in range(100):
        possible_moves = bagchal.get_possible_moves()

        input_vectors = bagchal.state_as_inputs(
            possible_moves, mode=6, rotate_board=True
        )

        turn = 1 if i % 2 == 0 else -1

        best_vector_index, pred_y = get_best_move(
            input_vectors, exploration=exploration, agent=turn
        )

        if rotate_board:
            best_move_index = best_vector_index // 7

            states.append(input_vectors[best_move_index * 7 + 0])
            y_preds.append(pred_y)
            states.append(input_vectors[best_move_index * 7 + 1])
            y_preds.append(pred_y)
            states.append(input_vectors[best_move_index * 7 + 2])
            y_preds.append(pred_y)
            states.append(input_vectors[best_move_index * 7 + 3])
            y_preds.append(pred_y)
            states.append(input_vectors[best_move_index * 7 + 4])
            y_preds.append(pred_y)
            states.append(input_vectors[best_move_index * 7 + 5])
            y_preds.append(pred_y)
            states.append(input_vectors[best_move_index * 7 + 6])
            y_preds.append(pred_y)

        else:
            best_move_index = best_vector_index
            states.append(input_vectors[best_move_index])
            y_preds.append(pred_y)

        bagchal = possible_moves[best_move_index].resulting_state

        if bagchal.game_status_check().decided:
            break

    nr_rewards = reward_transformer(
        bagchal.move_reward_goat(),
        bagchal.move_reward_tiger(),
        False,
    )

    rewards = td_reward_transformer(
        bagchal.move_reward_goat(),
        bagchal.move_reward_tiger(),
        states,
        y_preds,
        rotate_board,
    )

    print(f"Rewards: {len(rewards)}")
    print(f"States: {len(states)}")

    print(f"Before Trans:")
    print(f"{bagchal.move_reward_goat()}")
    print(f"{bagchal.move_reward_tiger()}")
    print(f"Rotated:")
    print(f"{rewards}")
    print(f"Not Rotated:")
    print(f"{nr_rewards}")

    # filtered_state = states
    # filtered_reward = rewards
    # filtered_y_pred = y_preds

    turn_filtered_state = []
    turn_filtered_reward = []
    turn_filtered_y_pred = []

    for index in range(len(states)):
        reward = rewards[index]
        state = states[index]
        y_pred = y_preds[index]

        is_goat = index % (7 * 2) < 7

        if (only_record == -1 and not is_goat) or (only_record == 1 and is_goat):
            turn_filtered_reward.append(reward)
            turn_filtered_y_pred.append(y_pred)
            turn_filtered_state.append(state)

    if not record_explorations:
        filtered_state = []
        filtered_reward = []
        filtered_y_pred = []

        for index in range(len(turn_filtered_state)):
            reward = turn_filtered_reward[index]
            state = turn_filtered_state[index]
            y_pred = turn_filtered_y_pred[index]

            if y_pred != None:
                filtered_reward.append(reward)
                filtered_y_pred.append(y_pred)
                filtered_state.append(state)
    else:
        filtered_state = turn_filtered_state
        filtered_reward = turn_filtered_reward
        filtered_y_pred = turn_filtered_y_pred

    sar_pair = list(zip(filtered_state, filtered_reward))
    # random.shuffle(sar_pair)

    return (sar_pair, y_preds, bagchal)


# params: exploration, train_on
# returns: (
#   number_of_positions,
#   number_of_trained_positions,
#   games_played,
#   goat_wons,
#   tiger_wons,
#   draws
# )
def training_step(
    exploration=True, train_on=None
) -> Tuple[int, int, int, int, int, int]:
    if train_on == -1:
        model = tiger_model
    elif train_on == 1:
        model = goat_model
    else:
        raise Exception("Must provide `train_on` parameter to `training_step()`")

    sar_pairs = []

    games_played = 0
    tiger_wons = 0
    goat_wons = 0
    draws = 0

    while len(sar_pairs) < 512:
        print(f"Training Step: {len(sar_pairs)}/512")
        (sar_pair, _, game_obj,) = play_game(
            exploration=exploration,
            only_record=train_on,
        )

        games_played += 1
        if game_obj.game_state() == libbaghchal.GameStatus.GoatWon:
            goat_wons += 1
        elif game_obj.game_state() == libbaghchal.GameStatus.TigerWon:
            tiger_wons += 1
        else:
            draws += 1

        f = open("sarpar.py", "a")
        f.write(str(sar_pair))
        f.close()
        exit()
        # print(f"SAR PAIR LENGTH: {}")
        sar_pairs += sar_pair

    positions_count = len(sar_pairs)

    number_of_pairs_to_choose = int(len(sar_pairs) * SAMPLE_RATE)
    sar_pairs = random.sample(sar_pairs, number_of_pairs_to_choose)

    states = []
    rewards = []
    for item in sar_pairs:
        states.append(item[0])
        rewards.append(item[1])

    model.fit(
        states,
        rewards,
        use_multiprocessing=True,
        batch_size=8,
    )

    return (positions_count, len(sar_pairs), games_played, goat_wons, tiger_wons, draws)


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
        for _ in range(3):
            (
                played_positions,
                trained_positions,
                t_games,
                t_goat_wons,
                t_tiger_wons,
                t_draws,
            ) = training_step(train_on=1)

            positions_counter += played_positions
            goat_trained_states += trained_positions
            game_counter += t_games
            goat_wins += t_goat_wons
            tiger_wins += t_tiger_wons
            draws += t_draws

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

            positions_counter += played_positions
            tiger_trained_states += trained_positions
            game_counter += t_games
            goat_wins += t_goat_wons
            tiger_wins += t_tiger_wons
            draws += t_draws

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

        (_, _, bagchal,) = play_game(
            exploration=False,
        )

        print(f"---------------------------------------------------")
        print(f"SAMPLE GAME:")
        print(f"---------------------------------------------------")
        print(f"http://localhost:3000/analysis?pgn={bagchal.pgn()}")
        print(f"---------------------------------------------------")
