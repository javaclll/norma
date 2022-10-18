import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf


class NormaModel(tf.keras.Sequential):
    # def train_step(self, data, y_pred=None):
    #     # Unpack the data. Its structure depends on your model and
    #     # on what you pass to `fit()`.
    #     x, y = data
    #
    #     print("Hollas")
    #
    #     with tf.GradientTape() as tape:
    #         if not y_pred:
    #             y_pred = self(x, training=True)  # Forward pass
    #         # Compute the loss value
    #         # (the loss function is configured in `compile()`)
    #         loss = self.compiled_loss(y, y_pred, regularization_losses=self.losses) # type: ignore
    #
    #     # Compute gradients
    #     trainable_vars = self.trainable_variables
    #     gradients = tape.gradient(loss, trainable_vars)
    #     # Update weights
    #     self.optimizer.apply_gradients(zip(gradients, trainable_vars))
    #     # Update metrics (includes the metric that tracks the loss)
    #     self.compiled_metrics.update_state(y, y_pred)  # type: ignore
    #     # Return a dict mapping metric names to current value
    #     return {m.name: m.result() for m in self.metrics}
    pass


model = NormaModel(
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
