from random import random

from h5py._hl.group import numpy

from norma.models import Models
from norma.utils import get_or_none, get_or_zero, two_in_one_merge

GOAT_EXPLORATION_FACTOR = 0.15
TIGER_EXPLORATION_FACTOR = 0.15
DISCOUNT_FACTOR = 0.90
TDN = 2
SAMPLE_RATE = 0.90


def reward_discounter(rewards, states):
    n = len(rewards)

    for index, value in enumerate(rewards[::-1]):
        for i in range(n - index - 1):
            rewards[n - i - 2 - index] += value * pow(1 - DISCOUNT_FACTOR, i + 1)

    return rewards


def advantage_calculator(rewards_g, rewards_t, states, models: Models):
    rewards_t.pop(0)

    rewards_g = two_in_one_merge(rewards_g)
    rewards_t = two_in_one_merge(rewards_t)

    rewards = []

    for i in range(len(rewards_g)):
        ith_re_g = get_or_none(rewards_g, i)
        ith_re_t = get_or_none(rewards_t, i)

        if ith_re_g is not None:
            rewards.append(ith_re_g)

        if ith_re_t is not None:
            rewards.append(ith_re_t)

    td_errors = []
    for index, observed_rewards in enumerate(rewards):
        if index % 2 != 0:
            model = models.tiger_critic_model
        elif index >= 20:
            model = models.goat_critic_model
        else:
            model = models.placement_critic_model

        original_state = states[index]
        resulting_state = get_or_none(states, index + 2)

        symmetry_choosen = numpy.random.randint(0, 6)

        if resulting_state:
            resulting_state = resulting_state[symmetry_choosen]
            original_state = original_state[symmetry_choosen]
            error = (
                observed_rewards
                + DISCOUNT_FACTOR * model.predict([resulting_state])  # type: ignore
                - model.predict([original_state])
            )
            td_errors.append(error)
        else:
            td_errors.append(
                observed_rewards - model.predict([original_state[symmetry_choosen]])
            )

    return td_errors
