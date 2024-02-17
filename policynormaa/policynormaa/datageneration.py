from functools import reduce
import math
from random import random, randint
from libbaghchal import Baghchal
from .helpers import movestoAction
from .abopponent import MiniMax
from .model import Model
from collections import deque
import numpy as np
from .constants import *

# XXX TODO: Find ways to fix whatever is not working, mainly on the model : find ways to incorporate rewards into the prediction


class Generator:
    def __init__(
        self,
        target_g_model=Model(),
        main_g_model=Model(),
        target_t_model=Model(),
        main_t_model=Model(),
    ):
        self.mm_agent = MiniMax()

        self.replay_goat_memory = deque(maxlen=MAXLEN)
        self.replay_tiger_memory = deque(maxlen=MAXLEN)
        self.randomness = MAX_EPSILON
        self.g_m_model = main_g_model
        self.t_m_model = main_t_model
        self.g_t_model = target_g_model
        self.t_t_model = target_t_model

    def generate(self, no_sims=NUMSIMS, sim_start=0):
        # initialize target models with main models

        self.g_t_model._model.set_weights(self.g_m_model._model.get_weights())
        self.t_t_model._model.set_weights(self.t_m_model._model.get_weights())

        # last time since update
        g_since_update = 0
        t_since_update = 0

        for i in range(sim_start, sim_start + no_sims):
            g_game = Baghchal.default()
            g_game.set_rewards(*REWARDS)

            t_game = Baghchal.default()
            t_game.set_rewards(*REWARDS)

            g_end = False
            t_end = False

            o_g_future_action = -1
            o_t_future_action = -1

            o_g_reward = 0
            o_t_reward = 0

            while not g_end:
                print(f"No of Sims: {i + 1}")
                print(f"Time Since Update: {g_since_update}")
                print()

                g_since_update += 1

                g_flat_board = np.array(reduce(lambda z, y: z + y, g_game.board()))

                gg_board = (g_flat_board == 1) * 1
                tg_board = (g_flat_board == -1) * 1

                # print(f"Goat Captured : {g_game.goat_captured()}")
                g_goat_placed = np.zeros(21)
                g_goat_placed[g_game.goat_counter()] = 1

                g_tiger_trap = np.zeros(5)
                g_tiger_trap[g_game.trapped_tiger()] = 1

                g_goat_captured = np.zeros(6)
                g_goat_captured[g_game.goat_captured()] = 1

                g_turn = g_game.turn()

                if g_turn == 1:
                    g_move = self.compute_move(
                        game=g_game,
                        turn=g_turn,
                    )

                    g_move_eval = g_game.make_move(
                        source=g_move[0],
                        target=g_move[1],
                    )

                    if (
                        g_game.game_status_check().decided
                        or len(g_game.game_history()) > 100
                    ):
                        g_end = True

                    g_action = movestoAction(
                        source=g_move[0],
                        target=g_move[1],
                    )

                    g_flat_board = np.array(reduce(lambda z, y: z + y, g_game.board()))

                    gg_updated_board = (g_flat_board == 1) * 1
                    tg_updated_board = (g_flat_board == -1) * 1

                    g_updated_goat_placed = np.zeros(21)
                    g_updated_goat_placed[g_game.goat_counter()] = 1

                    g_updated_tiger_trap = np.zeros(5)
                    g_updated_tiger_trap[g_game.trapped_tiger()] = 1

                    g_updated_goat_captured = np.zeros(6)
                    g_updated_goat_captured[g_game.goat_captured()] = 1

                    g_possible_moves = g_game.get_possible_moves()

                    if g_game.turn() == -1 and not g_end:
                        g_move = self.compute_move(
                            game=g_game,
                            turn=g_turn,
                            minimax=True,
                        )

                        g_move_eval = g_game.make_move(
                            source=g_move[0],
                            target=g_move[1],
                        )

                        print(f"Game Status is: {g_game.game_status_check().decided}")
                        if (
                            g_game.game_status_check().decided
                            or len(g_game.game_history()) > 100
                        ):
                            g_end = True

                        o_g_future_action = movestoAction(
                            source=g_move[0],
                            target=g_move[1],
                        )
                        o_g_reward = g_game.move_reward_tiger()[-1]

                    input_nodes = np.concatenate(
                        (
                            gg_board,
                            tg_board,
                            g_tiger_trap,
                            g_goat_captured,
                            g_updated_goat_placed,
                            g_action,
                            gg_updated_board,
                            tg_updated_board,
                            g_updated_tiger_trap,
                            g_updated_goat_captured,
                            g_updated_goat_placed,
                            g_game.move_reward_goat()[-1],
                            g_end,
                            o_g_future_action,
                            o_g_reward,
                        ),
                        axis=None,
                    ).reshape((1, -1))

                    self.replay_goat_memory.append([g_possible_moves, input_nodes])

                else:
                    g_end = True

                if g_since_update % 4 == 0 or g_end:
                    print("Goat Training !")
                    Model.training(
                        memory=self.replay_goat_memory,
                        m_model=self.g_m_model,
                        opponent_t_model=self.t_t_model,
                        end=g_end,
                    )

                if g_end:
                    self.g_m_model._model.save(GOATMODELPATH)
                    print(
                        f"Target Models Saved at {g_since_update} targets and {i + 1} sims"
                    )

            self.randomness = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * np.exp(
                -DECAY * (i + 1)
            )

    def compute_move(self, game: Baghchal, turn, minimax=False):
        if minimax:
            _, move = self.mm_agent.best_move(board=game)

        else:
            possible_moves = game.get_possible_moves()

            rand_number = random()

            if rand_number <= self.randomness:
                rand_number = randint(0, len(possible_moves) - 1)

                # use a random integer and then return the possible Move
                move = possible_moves[rand_number].move

            else:
                actions = []
                for move in possible_moves:
                    actions.append(movestoAction(move.move[0], move.move[1]))

                if turn == 1:
                    prediction = self.g_m_model.predict(game)[0]
                else:
                    prediction = self.t_m_model.predict(game)[0]

                action = np.argmax(prediction)

                while action not in actions:
                    prediction[action] = -math.inf
                    action = np.argmax(prediction)

                moveIndex = actions.index(action)

                move = possible_moves[moveIndex].move

        return move
