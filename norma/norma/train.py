from typing import List, Tuple

import libbaghchal
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

from .models import Models, models
from .reward import advantage_calculator
from .stats import Stats


def get_move(vectors: List, model: tf.keras.Model) -> Tuple[int, List, int]:
    symmetry_chosen = np.random.random_integers(0, 6)
    # symmetry_chosen = 0
    vector = vectors[symmetry_chosen]
    print(f"{vector}")
    pred = model.predict([vector])
    norm = np.linalg.norm(pred)

    pred = pred / norm

    print(f"{pred}")
    p = tf.nn.softmax(pred[0])
    print(f"{p}")
    p = np.array(p)
    print(f"{p}")

    # p = tf.divide(p, p.sum())

    action = np.random.choice(np.arange(pred[0].size), p=p)

    return action, pred, symmetry_chosen


def play_game(models: Models) -> Tuple[List, List, List, List, List, int, str]:
    states = []
    stages = []
    actions = []
    preds = []
    won_by = 0

    bagchal = libbaghchal.Baghchal.default()

    bagchal.set_game_over_on_invalid(state=True)

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
        gt_invalid_move=-100,
    )

    for _ in range(100):
        if bagchal.turn() == -1:
            model = models.tiger_actor_model
            i2m = libbaghchal.Baghchal.i2m_tiger
            stage = 0
        elif bagchal.turn() == 1 and bagchal.goat_counter() < 20:
            model = models.placement_actor_model
            i2m = libbaghchal.Baghchal.i2m_placement
            stage = 1
        else:
            model = models.goat_actor_model
            i2m = libbaghchal.Baghchal.i2m_goat
            stage = 2

        input_vector = bagchal.state_as_input_actor(None, mode=6, rotate_board=True)

        index, pred, symmetry_choosen = get_move(vectors=input_vector, model=model)

        source, destination = i2m(index)

        states.append(bagchal.index_to_input(index, symmetry=symmetry_choosen))
        stages.append(stage)
        actions.append(index)

        preds.append(pred)

        move_result = bagchal.make_move_with_symmetry(
            source=source, target=destination, symmetry=symmetry_choosen
        )

        game_status = bagchal.game_status_check()

        if not move_result.is_valid:
            print(f"Invalid move!")
            print(f"Decided: {game_status.decided}")

        if game_status.decided:
            print(f"Game deciced!")
            won_by = game_status.won_by
            break

    advantages = advantage_calculator(
        bagchal.move_reward_goat(), bagchal.move_reward_tiger(), states, models
    )

    # saa_pair = list(zip(states, advantages))
    # random.shuffle(saa_pair)

    return (states, actions, stages, advantages, preds, won_by, bagchal.pgn())


def index_to_action_vector(index: int, stage: int):
    if stage == 0:
        vec = np.zeros(192)
    elif stage == 1:
        vec = np.zeros(25)
    elif stage == 2:
        vec = np.zeros(112)
    else:
        raise Exception("Invalid action index!")

    vec[index] = 1

    return vec


def train_step(states, actions, stages, advantages, y_preds, pgn):
    print("Train Step!")
    print(f"States: {len(states)}")
    print(f"Stages: {len(stages)}")
    print(f"Advantages: {len(advantages)}")
    print(f"Y Preds: {len(y_preds)}")
    print(f"PGN: {pgn}")

    actor_losses = []
    critic_losses = []

    for i in range(len(states)):
        state = states[i]
        stage = stages[i]
        advantage = advantages[i]
        action = actions[i]

        if stage == 0:
            actor_model = models.tiger_actor_model
            critic_model = models.tiger_critic_model
        elif stage == 1:
            actor_model = models.placement_actor_model
            critic_model = models.placement_critic_model
        else:
            actor_model = models.goat_actor_model
            critic_model = models.goat_critic_model

        inp_tensor = tf.convert_to_tensor([state[0]])

        with tf.GradientTape() as tape:
            values = critic_model(inp_tensor, training=True)
            huber_loss = tf.keras.losses.Huber()
            critic_loss = huber_loss(values, advantage)

        critic_grads = tape.gradient(
            critic_loss,
            critic_model.trainable_variables,
        )

        critic_model.optimizer.apply_gradients(
            zip(
                critic_grads,
                critic_model.trainable_variables,
            )
        )

        with tf.GradientTape() as tape:
            actor_logits = actor_model(inp_tensor, training=True)

            norm = np.linalg.norm(actor_logits)  # type: ignore
            normalized_actor_logits = actor_logits / norm
            action_probabilities = tf.nn.softmax(normalized_actor_logits)

            actions_one_hot = index_to_action_vector(action, stage)
            # print(f"Probs: {action_probabilities}")
            # print(f"OneHot: {actions_one_hot}")
            chosen_action_probabilities = tf.reduce_sum(
                actions_one_hot * action_probabilities, axis=1
            )

            log_probs = tf.math.log(chosen_action_probabilities)
            # print(f"ERRR: {chosen_action_probabilities}")
            # print(f"ERRR: {log_probs}")
            # print(f"ERRR: {advantage}")
            # print(f"ERRR: {-tf.reduce_mean(log_probs * advantage)}")
            actor_loss = -tf.reduce_mean(log_probs * advantage)

        print(f"Actor Loss: {actor_loss}")
        actor_grads = tape.gradient(
            actor_loss,
            actor_model.trainable_variables,
        )

        actor_model.optimizer.apply_gradients(
            zip(
                actor_grads,
                actor_model.trainable_variables,
            )
        )

        actor_losses.append(float(actor_loss))
        critic_losses.append(float(critic_loss))

    print("Losses:")
    print(f"Actor: {actor_losses}")
    print(f"Critic: {critic_losses}")
    return (actor_losses, critic_losses)


def training_step() -> Tuple[int, int, int, int, int, int]:  # type: ignore
    played_positions = 0
    trained_positions = 0
    t_games = 0
    t_goat_wons = 0
    t_tiger_wons = 0
    t_draws = 0

    # for _ in range(512):
    for _ in range(1):
        (states, actions, stages, advatages, y_preds, won_by, pgn) = play_game(models)

        train_step(
            states=states,
            actions=actions,
            advantages=advatages,
            stages=stages,
            y_preds=y_preds,
            pgn=pgn,
        )

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
        ) = training_step()

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
        #
        # # Tiger Training
        # for _ in range(1):
        #     (
        #         played_positions,
        #         trained_positions,
        #         t_games,
        #         t_goat_wons,
        #         t_tiger_wons,
        #         t_draws,
        #     ) = training_step()
        #
        #     stats.add(
        #         game_counter=t_games,
        #         positions_counter=played_positions,
        #         goat_wins=t_goat_wons,
        #         tiger_wins=t_tiger_wons,
        #         draws=t_draws,
        #         tiger_trained_states=trained_positions,
        #         goat_trained_states=0,
        #         loss=1,
        #     )

        models.save_models()
