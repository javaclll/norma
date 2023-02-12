import os

# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from keras import layers
import tensorflow as tf


def build_model():
    inputs = tf.keras.Input(shape=(131,))
    d1 = layers.Dense(256, activation="leaky_relu")(inputs)
    d2 = layers.Dense(128, activation="leaky_relu")(d1)
    d3 = layers.Dense(128, activation="leaky_relu")(d2)
    d4 = layers.Dense(64, activation="leaky_relu")(d3)
    output = layers.Dense(1, activation="linear")(d4)

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
