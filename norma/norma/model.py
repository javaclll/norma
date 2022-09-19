import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf


model = tf.keras.Sequential(
    [
        tf.keras.layers.Dense(
            128,
            activation="relu",
            input_shape=(72,),
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

def load_model():
    if os.path.exists("weights/magma.index"):
        model.load_weights("weights/magma")
    else:
        model.save_weights("weights/magma")
