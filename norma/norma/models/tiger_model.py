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


tiger_actor_model = build_actor_model()


print("\n-----------------------------------")
print("Tiger Actor Model:")
print("-----------------------------------")
tiger_actor_model.summary()


tiger_critic_model = build_critic_model()

print("\n-----------------------------------")
print("Goat Critic Model:")
print("-----------------------------------")
tiger_critic_model.summary()


tiger_optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
tiger_actor_loss = tf.keras.losses.CategoricalCrossentropy()
tiger_critic_loss = tf.keras.losses.MeanSquaredError()


def load_model(name="magma"):
    if os.path.exists(f"weights/{name}/tiger_actor.index"):
        tiger_actor_model.load_weights(f"weights/{name}/tiger_actor")
    else:
        tiger_actor_model.save_weights(f"weights/{name}/tiger_actor")

    if os.path.exists(f"weights/{name}/tiger_critic.index"):
        tiger_critic_model.load_weights(f"weights/{name}/tiger_critic")
    else:
        tiger_critic_model.save_weights(f"weights/{name}/tiger_critic")
