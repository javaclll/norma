from abc import abstractmethod
from libbaghchal import Baghchal
import math
import random
from tabnanny import verbose
from .helpers import movestoAction
import numpy as np
import tensorflow as tf
from tensorflow import keras
from functools import reduce
from sklearn import preprocessing
import os

# Constants
DISCOUNTFACTOR = 0.7
OBSERVATIONSPACE = 82
SEQUENCESPACE = 169
ACTIONSPACE = 121
AFFECTFACTOR = 0.7
BATCHSIZE = 512

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
tf.compat.v1.disable_eager_execution()


class Model:
    def __init__(self, _model=None):
        if _model:
            self._model = _model
        else:
            optimizer = keras.optimizers.legacy.Adam(learning_rate=0.001)
            initializer = keras.initializers.HeUniform()

            self._model = keras.Sequential()

            self._model.add(
                keras.layers.Dense(
                    70, input_shape=(OBSERVATIONSPACE,), kernel_initializer=initializer
                )
            )
            self._model.add(keras.layers.LeakyReLU(alpha=0.3))
            self._model.add(
                keras.layers.Dense(
                    int(OBSERVATIONSPACE * DISCOUNTFACTOR),
                    kernel_initializer=initializer,
                )
            )
            self._model.add(keras.layers.LeakyReLU(alpha=0.3))
            self._model.add(
                keras.layers.Dense(
                    ACTIONSPACE, activation="linear", kernel_initializer=initializer
                )
            )
            self._model.compile(
                optimizer=optimizer, loss=keras.losses.Huber(), metrics=["accuracy"]
            )

            self._model.summary()

    def predict(self, game: Baghchal):
        flat_board = np.array(reduce(lambda z, y: z + y, game.board()))
        g_board = (flat_board == 1) * 1
        t_board = (flat_board == -1) * 1

        goat_captured = np.zeros(6)

        goat_captured[game.goat_captured()] = 1

        goat_placed = np.zeros(21)
        goat_placed[game.goat_counter()] = 1

        tiger_trapped = np.zeros(5)
        tiger_trapped[game.trapped_tiger()] = 1

        tensor = np.concatenate(
            (
                g_board,
                t_board,
                goat_placed,
                tiger_trapped,
                goat_captured,
            ),
            axis=None,
        )

        prediction = self._model.predict(tensor.reshape(1, -1))
        # prediction = preprocessing.normalize(prediction, axis=1)
        print(f"Predicted Value is: {prediction.shape}")
        return prediction

    @abstractmethod
    def training(memory, m_model, opponent_t_model, end):
        no_data = len(memory)

        if no_data < BATCHSIZE:
            return

        mini_batch = random.sample(memory, BATCHSIZE)
        batch_possible_moves = []
        mini_memory = []

        for data in mini_batch:
            batch_possible_moves.append(data[0])
            mini_memory.append(data[1])

        print(mini_batch[0][1][0][0:OBSERVATIONSPACE])
        print(mini_batch[0][1][0][OBSERVATIONSPACE + 1 : (OBSERVATIONSPACE * 2) + 1])

        current_state = np.array([data[0][0:OBSERVATIONSPACE] for data in mini_memory])
        current_action_predict = m_model._model.predict(current_state)

        future_state = np.array(
            [
                data[0][OBSERVATIONSPACE + 1 : OBSERVATIONSPACE + OBSERVATIONSPACE + 1]
                for data in mini_memory
            ]
        )
        # o_future_action_predict = opponent_t_model.model.predict(future_state)

        train_x = np.zeros((BATCHSIZE, OBSERVATIONSPACE))
        train_y = np.zeros((BATCHSIZE, ACTIONSPACE))

        for index, data in enumerate(mini_memory):
            if not data[0][-3]:
                # actions = []
                # action = np.argmax(o_future_action_predict[index])

                # for move in batch_possible_moves[index]:
                #     actions.append(movestoAction(move["move"][0], move["move"][1]))

                # while action not in actions:
                #     o_future_action_predict[index][action] = -math.inf
                #     action = np.argmax(o_future_action_predict[index])

                max_future_reward = data[0][-2] - DISCOUNTFACTOR * (data[0][-1])

            else:
                # Max Future reward can be extracted from the minimax algorithm
                max_future_reward = data[0][-2]

            training_reward = current_action_predict[index]

            training_reward[int(data[0][OBSERVATIONSPACE])] = (
                1 - AFFECTFACTOR
            ) * training_reward[
                int(data[0][OBSERVATIONSPACE])
            ] + AFFECTFACTOR * max_future_reward

            train_x[index, :] = data[0][0:OBSERVATIONSPACE]
            train_y[index, :] = training_reward

        m_model._model.fit(
            train_x, train_y, batch_size=BATCHSIZE, verbose=2, shuffle=True
        )
