import os

import tensorflow as tf
from keras import layers

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


def build_actor_model():
    inputs = tf.keras.Input(shape=(131,))

    board = tf.keras.layers.Reshape((5, 5, 3))(inputs[:, :75])  # type: ignore
    scalar = tf.keras.layers.Reshape((6,))(inputs[:, 125:])  # type: ignore

    conv_board = layers.Conv2D(64, (3, 3), activation="relu")(board)
    conv_board = layers.Conv2D(64, (3, 3), activation="relu")(conv_board)
    conv_board = layers.MaxPooling2D((2, 2), padding="same")(conv_board)
    conv_board = layers.Flatten()(conv_board)

    concat = layers.concatenate([conv_board, scalar])

    fc1 = layers.Dense(128, activation="relu")(concat)
    fc2 = layers.Dense(64, activation="relu")(fc1)
    output = layers.Dense(112, activation="softmax")(fc2)

    return tf.keras.Model(inputs=inputs, outputs=output)


def build_critic_model():
    inputs = tf.keras.Input(shape=(131,))

    board = tf.keras.layers.Reshape((5, 5, 5))(inputs[:, :125])  # type: ignore
    scalar = tf.keras.layers.Reshape((6,))(inputs[:, 125:])  # type: ignore

    conv_board = layers.Conv2D(64, (3, 3), activation="relu")(board)
    conv_board = layers.Conv2D(64, (3, 3), activation="relu")(conv_board)
    conv_board = layers.MaxPooling2D((2, 2), padding="same")(conv_board)
    conv_board = layers.Flatten()(conv_board)

    concat = layers.concatenate([conv_board, scalar])

    fc1 = layers.Dense(128, activation="relu")(concat)
    fc2 = layers.Dense(64, activation="relu")(fc1)
    output = layers.Dense(1, activation="linear")(fc2)

    return tf.keras.Model(inputs=inputs, outputs=output)


def build_placement_actor_model():
    inputs = tf.keras.Input(shape=(131,))

    board = tf.keras.layers.Reshape((5, 5, 3))(inputs[:, :75])  # type: ignore
    scalar = tf.keras.layers.Reshape((6,))(inputs[:, 125:])  # type: ignore

    conv_board = layers.Conv2D(64, (3, 3), activation="relu")(board)
    conv_board = layers.Conv2D(64, (3, 3), activation="relu")(conv_board)
    conv_board = layers.MaxPooling2D((2, 2), padding="same")(conv_board)
    conv_board = layers.Flatten()(conv_board)

    concat = layers.concatenate([conv_board, scalar])

    fc1 = layers.Dense(128, activation="relu")(concat)
    fc2 = layers.Dense(64, activation="relu")(fc1)
    output = layers.Dense(25, activation="softmax")(fc2)

    return tf.keras.Model(inputs=inputs, outputs=output)


def build_placement_critic_model():
    inputs = tf.keras.Input(shape=(131,))

    board = tf.keras.layers.Reshape((5, 5, 3))(inputs[:, :75])  # type: ignore
    move = tf.keras.layers.Reshape((5, 5, 2))(inputs[:, 75:125])  # type: ignore
    scalar = tf.keras.layers.Reshape((6,))(inputs[:, 125:])  # type: ignore

    conv_board = layers.Conv2D(64, (3, 3), activation="relu")(board)
    conv_board = layers.Conv2D(64, (3, 3), activation="relu")(conv_board)
    conv_board = layers.MaxPooling2D((2, 2), padding="same")(conv_board)
    conv_board = layers.Flatten()(conv_board)

    conv_move = layers.Conv2D(64, (3, 3), activation="relu")(move)
    conv_move = layers.Conv2D(64, (3, 3), activation="relu")(conv_move)
    conv_move = layers.MaxPooling2D((2, 2), padding="same")(conv_move)
    conv_move = layers.Flatten()(conv_move)

    concat = layers.concatenate([conv_board, conv_move, scalar])

    fc1 = layers.Dense(128, activation="relu")(concat)
    fc2 = layers.Dense(64, activation="relu")(fc1)
    output = layers.Dense(1, activation="linear")(fc2)

    return tf.keras.Model(inputs=inputs, outputs=output)


goat_actor_model = build_actor_model()

# goat_actor_model.compile(
#     optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
#     loss="mean_squared_error",
# )


print("\n-----------------------------------")
print("Goat Actor Model:")
print("-----------------------------------")
goat_actor_model.summary()


goat_critic_model = build_critic_model()

# goat_critic_model.compile(
#     optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
#     loss="mean_squared_error",
# )

print("\n-----------------------------------")
print("Goat Critic Model:")
print("-----------------------------------")
goat_critic_model.summary()

placement_actor_model = build_placement_actor_model()

# placement_actor_model.compile(
#     optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
#     loss="mean_squared_error",
# )


print("\n-----------------------------------")
print("Placement Actor Model:")
print("-----------------------------------")
placement_actor_model.summary()


placement_critic_model = build_placement_critic_model()

# placement_critic_model.compile(
#     optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
#     loss="mean_squared_error",
# )

print("\n-----------------------------------")
print("Placement Critic Model:")
print("-----------------------------------")
placement_critic_model.summary()

goat_optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
goat_actor_loss = tf.keras.losses.CategoricalCrossentropy()
goat_critic_loss = tf.keras.losses.MeanSquaredError()


def load_model(name="magma"):
    if os.path.exists(f"weights/{name}/goat_actor.index"):
        goat_actor_model.load_weights(f"weights/{name}/goat_actor")
    else:
        goat_actor_model.save_weights(f"weights/{name}/goat_actor")

    if os.path.exists(f"weights/{name}/goat_critic.index"):
        goat_critic_model.load_weights(f"weights/{name}/goat_critic")
    else:
        goat_critic_model.save_weights(f"weights/{name}/goat_critic")

    if os.path.exists(f"weights/{name}/placement_actor.index"):
        goat_critic_model.load_weights(f"weights/{name}/placement_actor")
    else:
        goat_critic_model.save_weights(f"weights/{name}/placement_actor")

    if os.path.exists(f"weights/{name}/placement_critic.index"):
        goat_critic_model.load_weights(f"weights/{name}/placement_critic")
    else:
        goat_critic_model.save_weights(f"weights/{name}/placement_critic")
