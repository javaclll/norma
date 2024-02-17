import os

import tensorflow as tf

from norma.models import goat_model, tiger_model

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
print("Num GPUs Available: ", len(tf.config.list_physical_devices("GPU")))

# Test if GPU is available by matmul
with tf.device("/GPU:0"):  # type: ignore
    a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])

# Run on the GPU
c = tf.matmul(a, b)
print(c)


class Models:
    def __init__(
        self,
        goat_actor_model: tf.keras.Model,
        tiger_actor_model: tf.keras.Model,
        placements_actor_model: tf.keras.Model,
        goat_critic_model: tf.keras.Model,
        tiger_critic_model: tf.keras.Model,
        placement_critic_model: tf.keras.Model,
    ):
        self.goat_actor_model = goat_actor_model
        self.tiger_actor_model = tiger_actor_model
        self.placement_actor_model = placements_actor_model
        self.goat_critic_model = goat_critic_model
        self.tiger_critic_model = tiger_critic_model
        self.placement_critic_model = placement_critic_model

    def save_models(self):
        assert self.name, "No model has been loaded!"

        print(f"Saving model: {self.name}")

        self.goat_actor_model.save_weights(f"weights/{self.name}/goat_actor")
        self.goat_critic_model.save_weights(f"weights/{self.name}/goat_critic")
        self.tiger_actor_model.save_weights(f"weights/{self.name}/tiger_actor")
        self.tiger_critic_model.save_weights(f"weights/{self.name}/tiger_critic")
        self.placement_critic_model.save_weights(
            f"weights/{self.name}/placement_critic"
        )
        self.placement_actor_model.save_weights(f"weights/{self.name}/placement_actor")

    def load_models(self, name: str = "magma"):
        self.name = name

        # Goat Models
        if os.path.exists(f"weights/{name}/goat_actor.index"):
            self.goat_actor_model.load_weights(f"weights/{name}/goat_actor")
        else:
            self.goat_actor_model.save_weights(f"weights/{name}/goat_actor")

        if os.path.exists(f"weights/{name}/goat_critic.index"):
            self.goat_critic_model.load_weights(f"weights/{name}/goat_critic")
        else:
            self.goat_critic_model.save_weights(f"weights/{name}/goat_critic")

        # Placement Models
        if os.path.exists(f"weights/{name}/placement_actor.index"):
            self.placement_actor_model.load_weights(f"weights/{name}/placement_actor")
        else:
            self.placement_actor_model.save_weights(f"weights/{name}/placement_actor")

        if os.path.exists(f"weights/{name}/placement_critic.index"):
            self.placement_critic_model.load_weights(f"weights/{name}/placement_critic")
        else:
            self.placement_critic_model.save_weights(f"weights/{name}/placement_critic")

        # Tiger Models
        if os.path.exists(f"weights/{name}/tiger_actor.index"):
            self.tiger_actor_model.load_weights(f"weights/{name}/tiger_actor")
        else:
            self.tiger_actor_model.save_weights(f"weights/{name}/tiger_actor")

        if os.path.exists(f"weights/{name}/tiger_critic.index"):
            self.tiger_critic_model.load_weights(f"weights/{name}/tiger_critic")
        else:
            self.tiger_critic_model.save_weights(f"weights/{name}/tiger_critic")


models = Models(
    goat_actor_model=goat_model.goat_actor_model,
    tiger_actor_model=tiger_model.tiger_actor_model,
    placements_actor_model=goat_model.placement_actor_model,
    goat_critic_model=goat_model.goat_critic_model,
    tiger_critic_model=tiger_model.tiger_critic_model,
    placement_critic_model=goat_model.placement_critic_model,
)
