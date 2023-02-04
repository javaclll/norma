import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from keras import layers
import tensorflow as tf


class NormaModel(tf.keras.Sequential):
    pass


def build_model():
    input_board = tf.keras.Input(shape=(5, 5, 3))
    input_move = tf.keras.Input(shape=(5, 5, 2))
    input_scalar = tf.keras.Input(shape=(6,))

    conv_board = layers.Conv2D(32, (3, 3), activation="relu")(input_board)
    conv_board = layers.MaxPooling2D((2, 2))(conv_board)
    conv_board = layers.Flatten()(conv_board)

    conv_move = layers.Conv2D(32, (3, 3), activation="relu")(input_move)
    conv_move = layers.MaxPooling2D((2, 2))(conv_move)
    conv_move = layers.Flatten()(conv_move)

    concat = layers.concatenate([conv_board, conv_move, input_scalar])

    fc1 = layers.Dense(64, activation="relu")(concat)
    fc2 = layers.Dense(64, activation="relu")(fc1)
    output = layers.Dense(1, activation="linear")(fc2)

    return tf.keras.Model(
        inputs=[input_board, input_move, input_scalar], outputs=output
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
