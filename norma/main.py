import tensorflow as tf
from bagchal import Bagchal



class NormaModel(tf.keras.Sequential):
    pass

model = tf.keras.Sequential(
    [
        tf.keras.layers.InputLayer(input_shape=71),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(1),
    ]
)

model.compile(
    optimizer="adam",
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"],
)


bagchal = Bagchal.new()
