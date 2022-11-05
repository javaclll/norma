import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf


class NormaModel(tf.keras.Sequential):
    pass


# model = NormaModel(
#     [
#         tf.keras.layers.Dense(
#             64,
#             activation="leaky_relu",
#             input_shape=(64,),
#             kernel_initializer="random_normal",
#             bias_initializer="zeros",
#         ),
#         tf.keras.layers.Reshape((8, 8, 1)),
#         tf.keras.layers.Conv2D(8, kernel_size=(3, 3), activation="leaky_relu"),
#         tf.keras.layers.Reshape((288,)),
#         tf.keras.layers.Dense(
#             (128),
#             activation="leaky_relu",
#             kernel_initializer="random_normal",
#             bias_initializer="zeros",
#         ),
#         tf.keras.layers.Dense(
#             64,
#             activation="leaky_relu",
#             kernel_initializer="random_normal",
#             bias_initializer="zeros",
#         ),
#         tf.keras.layers.Dense(
#             32,
#             activation="leaky_relu",
#             kernel_initializer="random_normal",
#             bias_initializer="zeros",
#         ),
#         tf.keras.layers.Dense(
#             1,
#             kernel_initializer="random_normal",
#             bias_initializer="zeros",
#         ),
#     ]
# )

model = NormaModel(
    [
        tf.keras.layers.Dense(
            64,
            activation="leaky_relu",
            input_shape=(64,),
            kernel_initializer="random_normal",
            bias_initializer="zeros",
        ),
        tf.keras.layers.Reshape((8, 8, 1)),
        tf.keras.layers.Conv2D(8, kernel_size=(3, 3), activation="leaky_relu"),
        tf.keras.layers.Reshape((288,)),
        tf.keras.layers.Dense(
            (128),
            activation="leaky_relu",
            kernel_initializer="random_normal",
            bias_initializer="zeros",
        ),
        tf.keras.layers.Dense(
            64,
            activation="leaky_relu",
            kernel_initializer="random_normal",
            bias_initializer="zeros",
        ),
        tf.keras.layers.Dense(
            32,
            activation="leaky_relu",
            kernel_initializer="random_normal",
            bias_initializer="zeros",
        ),
        tf.keras.layers.Dense(
            1,
            activation="linear",
            kernel_initializer="random_normal",
            bias_initializer="zeros",
        ),
    ]
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="mean_squared_error",
)

model.summary()


def load_model():
    if os.path.exists("weights/magma.index"):
        model.load_weights("weights/magma")
    else:
        model.save_weights("weights/magma")
