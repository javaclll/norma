import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import numpy


import tensorflow as tf


model = tf.keras.Sequential(
    [
        tf.keras.layers.Dense(
            128,
            activation="relu",
            input_shape=(71,),
            kernel_initializer="random_normal",
            bias_initializer="zeros",
        ),
        tf.keras.layers.Dense(
            128,
            activation="relu",
            kernel_initializer="random_normal",
            bias_initializer="zeros",
        ),
        tf.keras.layers.Dense(
            128,
            activation="relu",
            kernel_initializer="random_normal",
            bias_initializer="zeros",
        ),
        tf.keras.layers.Dense(
            128,
            activation="relu",
            kernel_initializer="random_normal",
            bias_initializer="zeros",
        ),
        tf.keras.layers.Dense(
            1,
            kernel_initializer="random_normal",
            bias_initializer="zeros",
        ),
    ]
)

model.compile(
    optimizer="adam",
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"],
)


def get_best_move(possible_moves):
    inputs = numpy.asarray(possible_moves)
    predication = model.predict_on_batch(inputs)

    return predication.argmax()
