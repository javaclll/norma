import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from keras import layers
import tensorflow as tf


class NormaModel(tf.keras.Sequential):
    pass


def build_model():
    inputs = tf.keras.Input(shape=(131,))

    tiger_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, :25])  # type: ignore
    goat_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, 25:50])  # type: ignore
    blank_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, 50:75])  # type: ignore
    source_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, 75:100])  # type: ignore
    destination_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, 100:125])  # type: ignore
    scalar = tf.keras.layers.Reshape((6,))(inputs[:, 125:])  # type: ignore

    conv_goat_board = layers.Conv2D(32, (3, 3), activation="relu")(goat_board)
    conv_goat_board = layers.Conv2D(32, (3, 3), activation="relu")(conv_goat_board)
    conv_goat_board = layers.Flatten()(conv_goat_board)

    conv_tiger_board = layers.Conv2D(32, (3, 3), activation="relu")(tiger_board)
    conv_tiger_board = layers.Conv2D(32, (3, 3), activation="relu")(conv_tiger_board)
    conv_tiger_board = layers.Flatten()(conv_tiger_board)

    conv_blank_board = layers.Conv2D(32, (3, 3), activation="relu")(blank_board)
    conv_blank_board = layers.Conv2D(32, (3, 3), activation="relu")(conv_blank_board)
    conv_blank_board = layers.Flatten()(conv_blank_board)

    conv_source_board = layers.Conv2D(32, (3, 3), activation="relu")(source_board)
    conv_source_board = layers.Conv2D(32, (3, 3), activation="relu")(conv_source_board)
    conv_source_board = layers.Flatten()(conv_source_board)

    conv_destination_board = layers.Conv2D(32, (3, 3), activation="relu")(
        destination_board
    )
    conv_destination_board = layers.Conv2D(32, (3, 3), activation="relu")(
        conv_destination_board
    )
    conv_destination_board = layers.Flatten()(conv_destination_board)

    concat = layers.concatenate(
        [
            conv_goat_board,
            conv_tiger_board,
            conv_blank_board,
            conv_source_board,
            conv_destination_board,
            scalar,
        ]
    )

    fc1 = layers.Dense(128, activation="relu")(concat)
    fc2 = layers.Dense(64, activation="relu")(fc1)
    output = layers.Dense(1, activation="linear")(fc2)

    return tf.keras.Model(inputs=inputs, outputs=output)


tiger_model = build_model()

tiger_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="mean_squared_error",
)


print(f"\n-----------------------------------")
print(f"Tiger Model:")
print(f"-----------------------------------")
tiger_model.summary()


goat_model = build_model()

goat_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
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
