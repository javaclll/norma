from bagchal import Bagchal
# from bagchal.bagchal import GameState
# from model import model
# import numpy
# import random
# from copy import deepcopy
#
#
# EXPLORATION_FACTOR = 0.5
# DISCOUNT_FACTOR = 0.20
#
#
# def get_best_move(input_vectors):
#     inputs = numpy.asarray(input_vectors)
#
#     if random.uniform(0, 1) < EXPLORATION_FACTOR:
#         return random.randint(0, len(input_vectors) - 1)
#     else:
#         predication = model.predict_on_batch(inputs)
#         return predication.argmax()
#
#
# def reward_discounter(rewards):
#     n = len(rewards)
#     for (index, value) in enumerate(rewards[::-1]):
#         for i in range(n - index - 1):
#             rewards[n - i - 2 - index] += value * pow(DISCOUNT_FACTOR, i + 1)
#     return rewards
#
#
# def generate_training_batch(N=100):
#     for i in range(N):
#         states = []
#
#         bagchal = Bagchal.new()
#
#         while not bagchal.game_status_check()["decided"]:
#             try:
#                 possible_moves = bagchal.get_possible_moves()
#
#                 input_vectors = bagchal.state_as_inputs(possible_moves)
#
#                 best_move = get_best_move(input_vectors)
#
#                 states.append(input_vectors[best_move])
#
#                 bagchal = possible_moves[best_move]["resulting_state"]
#
#             except Exception as e:
#                 print(f"Possible Moves: {bagchal.get_possible_moves()}")
#                 print(f"Possible Moves: {bagchal.game_status_check()}")
#                 print(bagchal.turn)
#                 print(bagchal.board)
#                 raise e
#
#         # discounted_rewards_goat = reward_discounter(bagchal.move_reward_goat)
#         # discounted_rewards_tiger = reward_discounter(bagchal.move_reward_goat)
#
#         print(bagchal.move_reward_goat)
#         print(bagchal.move_reward_tiger)
#         if bagchal.game_state == GameState.GOAT_WON.value:
#             print("Goat Won")
#         else:
#             print("Tiger Won")
#
#
# print(generate_training_batch())
#
#
# # state, action, result
# # true
# # Reward must go back

bag = Bagchal.new()

print(bag.state_as_inputs())

def hello():
    pass
