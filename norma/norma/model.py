import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf


class NormaModel(tf.keras.Sequential):
    pass


def build_model():
    return NormaModel(
        [
            tf.keras.layers.Dense(
                100,
                activation="leaky_relu",
                input_shape=(64,),
                kernel_initializer="random_normal",
                bias_initializer="zeros",
            ),
            tf.keras.layers.Reshape((10, 10, 1)),
            tf.keras.layers.Conv2D(8, kernel_size=(3, 3), activation="leaky_relu"),
            tf.keras.layers.MaxPooling2D((3, 3)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(
                128,
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


tiger_model = build_model()

tiger_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
    loss="mean_squared_error",
)


print(f"\n-----------------------------------")
print(f"Tiger Model:")
print(f"-----------------------------------")
tiger_model.summary()


goat_model = build_model()

goat_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
    loss="mean_squared_error",
)

print(f"\n-----------------------------------")
print(f"Goat Model:")
print(f"-----------------------------------")
goat_model.summary()


def load_model(name="magma"):
    if os.path.exists(f"weights/{name}/tiger.index"):
        tiger_model.load_weights(f"weights/{name}/tiger")
    else:
        tiger_model.save_weights(f"weights/{name}/tiger")

    if os.path.exists(f"weights/{name}/goat.index"):
        goat_model.load_weights(f"weights/{name}/goat")
    else:
        tiger_model.save_weights(f"weights/{name}/goat")
