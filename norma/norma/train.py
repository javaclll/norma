import random
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
    vector = vectors[symmetry_chosen]
    pred = model.predict([vector])
    action = np.random.choice(np.arange(pred[0].size), p=pred[0])

    return (action, pred, symmetry_chosen)


def play_game(models: Models) -> Tuple[List, List, List, List, int]:
    states = []
    stages = []
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

        preds.append(pred)

        bagchal.make_move_with_symmetry(
            source=source, target=destination, symmetry=symmetry_choosen
        )

        game_status = bagchal.game_status_check()

        if game_status.decided:
            won_by = game_status.won_by
            break

    advantages = advantage_calculator(
        bagchal.move_reward_goat(), bagchal.move_reward_tiger(), states, models
    )

    # saa_pair = list(zip(states, advantages))
    # random.shuffle(saa_pair)

    return (states, stages, advantages, preds, won_by)


def train_step(
    states,
    stages,
    advantages,
    y_preds,
):
    """
    Train the Actor and Critic models using the Advantage.

    Args:
    - actor_model: The Actor model.
    - critic_model: The Critic model.
    - states: The batch of states.
    - actions: The batch of actions.
    - rewards: The batch of rewards.
    - next_states: The batch of next states.
    - done: The batch of done flags.
    - optimizer: The optimizer to use for training.
    - gamma: The discount factor.

    Returns:
    - actor_loss: The loss of the Actor model.
    - critic_loss: The loss of the Critic model.
    """

    # Compute the advantage for each sample in the batch
    # values = critic_model(states)
    # next_values = critic_model(next_states)
    # advantages = rewards + gamma * next_values * (1 - done) - values
    if stages == 0:
        actor_model = models.tiger_actor_model
        critic_model = models.tiger_critic_model
    elif stages == 1:
        actor_model = models.placement_actor_model
        critic_model = models.placement_critic_model
    else:
        actor_model = models.goat_actor_model
        critic_model = models.goat_critic_model

    # Compute the actor loss and apply the gradients
    with tf.GradientTape() as tape:
        # logits = actor_model(states)
        # dist = tfp.distributions.Categorical(logits=y_preds)
        # log_probs = dist.log_prob(actions)
        actor_loss = -tf.reduce_mean(y_preds * advantages)

    actor_gradients = tape.gradient(actor_loss, actor_model.trainable_variables)
    actor_model.apply_gradients(actor_gradients)
    # optimizer.apply_gradients(zip(actor_gradients, actor_model.trainable_variables))

    # Compute the critic loss and apply the gradients
    with tf.GradientTape() as tape:
        critic_loss = tf.reduce_mean(tf.square(advantages))
    critic_gradients = tape.gradient(critic_loss, critic_model.trainable_variables)
    critic_model.apply_gradients(critic_gradients)

    return actor_loss, critic_loss


def training_step(train_on: int) -> Tuple[int, int, int, int, int, int]:  # type: ignore
    played_positions = 0
    trained_positions = 0
    t_games = 0
    t_goat_wons = 0
    t_tiger_wons = 0
    t_draws = 0

    trainable_states = []
    trainable_stages = []
    trainable_advantages = []
    trainable_y_preds = []
    while len(trainable_states) < 512:
        (states, stages, advatages, y_preds, won_by) = play_game(models)

        trainable_states += states
        trainable_stages += stages
        trainable_y_preds += y_preds
        trainable_advantages += advatages

        played_positions += len(states) * 7
        t_games += 1
        if won_by == 1:
            t_goat_wons += 1
        elif won_by == -1:
            t_tiger_wons += 1
        else:
            t_draws += 1

    train_step(
        states=trainable_states,
        advatages=trainable_advantages,
        stages=trainable_stages,
        y_preds=trainable_y_preds,
    )

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

        models.save_models()
