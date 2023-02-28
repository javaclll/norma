from norma.models import Models
from norma.utils import get_or_none, two_in_one_merge

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


def reward_transformer(rewards_g, rewards_t, states, y_preds, models: Models):
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

    td_rewards = []
    td_error = []
    for observed_rewards, index in enumerate(rewards):
        if index  % 2 != 0:
            model = models.tiger_critic_model
        elif index > 20:
            model = models.placement_critic_model
        else:
            model = models.goat_citic_model


        td_reward = rewards + DISCOUNT_FACTOR * 

    return rewards
