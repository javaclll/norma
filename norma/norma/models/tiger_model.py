import os

import tensorflow as tf
from keras import layers


def build_actor_model():
    inputs = tf.keras.Input(shape=(131,))

    tiger_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, :25])  # type: ignore
    goat_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, 25:50])  # type: ignore
    blank_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, 50:75])  # type: ignore
    # source_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, 75:100])  # type: ignore
    # destination_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, 100:125])  # type: ignore
    scalar = tf.keras.layers.Reshape((6,))(inputs[:, 125:])  # type: ignore

    conv_goat_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(goat_board)
    conv_goat_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(conv_goat_board)
    conv_goat_board = layers.Flatten()(conv_goat_board)

    conv_tiger_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(tiger_board)
    conv_tiger_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(conv_tiger_board)
    conv_tiger_board = layers.Flatten()(conv_tiger_board)

    conv_blank_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(blank_board)
    conv_blank_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(conv_blank_board)
    conv_blank_board = layers.Flatten()(conv_blank_board)

    # conv_source_board = layers.Conv2D(32, (3, 3), activation="relu")(source_board)
    # conv_source_board = layers.Conv2D(32, (3, 3), activation="relu")(conv_source_board)
    # conv_source_board = layers.Flatten()(conv_source_board)
    #
    # conv_destination_board = layers.Conv2D(32, (3, 3), activation="relu")(
    #     destination_board
    # )
    # conv_destination_board = layers.Conv2D(32, (3, 3), activation="relu")(
    #     conv_destination_board
    # )
    # conv_destination_board = layers.Flatten()(conv_destination_board)

    concat = layers.concatenate(
        [
            conv_goat_board,
            conv_tiger_board,
            conv_blank_board,
            # conv_source_board,
            # conv_destination_board,
            scalar,
        ]
    )
    fc1 = layers.Dense(
        128, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(l=0.1)
    )(concat)
    fc2 = layers.Dense(
        64, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(l=0.1)
    )(fc1)
    output = layers.Dense(
        192, activation="linear", kernel_regularizer=tf.keras.regularizers.l2(l=0.1)
    )(fc2)

    return tf.keras.Model(name="TigerActor", inputs=inputs, outputs=output)


def build_critic_model():
    inputs = tf.keras.Input(shape=(131,))

    tiger_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, :25])  # type: ignore
    goat_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, 25:50])  # type: ignore
    blank_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, 50:75])  # type: ignore
    source_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, 75:100])  # type: ignore
    destination_board = tf.keras.layers.Reshape((5, 5, 1))(inputs[:, 100:125])  # type: ignore
    scalar = tf.keras.layers.Reshape((6,))(inputs[:, 125:])  # type: ignore

    conv_goat_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(goat_board)
    conv_goat_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(conv_goat_board)
    conv_goat_board = layers.Flatten()(conv_goat_board)

    conv_tiger_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(tiger_board)
    conv_tiger_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(conv_tiger_board)
    conv_tiger_board = layers.Flatten()(conv_tiger_board)

    conv_blank_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(blank_board)
    conv_blank_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(conv_blank_board)
    conv_blank_board = layers.Flatten()(conv_blank_board)

    conv_source_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(source_board)
    conv_source_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(conv_source_board)
    conv_source_board = layers.Flatten()(conv_source_board)

    conv_destination_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(destination_board)
    conv_destination_board = layers.Conv2D(
        32,
        (3, 3),
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(l=0.1),
    )(conv_destination_board)
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

    fc1 = layers.Dense(
        128, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(l=0.1)
    )(concat)
    fc2 = layers.Dense(
        64, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(l=0.1)
    )(fc1)
    output = layers.Dense(
        1, activation="linear", kernel_regularizer=tf.keras.regularizers.l2(l=0.1)
    )(fc2)

    return tf.keras.Model(name="TigerCritic", inputs=inputs, outputs=output)


tiger_actor_model = build_actor_model()
tiger_actor_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
)


print("\n-----------------------------------")
print("Tiger Actor Model:")
print("-----------------------------------")
tiger_actor_model.summary()


tiger_critic_model = build_critic_model()

optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
tiger_critic_model.compile(
    optimizer=optimizer,
    loss=tf.keras.losses.MeanSquaredError(),
)

print("\n-----------------------------------")
print("Goat Critic Model:")
print("-----------------------------------")
tiger_critic_model.summary()
