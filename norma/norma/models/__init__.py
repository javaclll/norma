import tensorflow as tf

from norma.models import goat_model, tiger_model


class Models:
    def __init__(
        self,
        goat_actor_model: tf.keras.Model,
        tiger_actor_model: tf.keras.Model,
        placements_actor_model: tf.keras.Model,
        goat_citic_model: tf.keras.Model,
        tiger_critic_model: tf.keras.Model,
        placement_critic_model: tf.keras.Model,
    ):
        self.goat_actor_model = goat_actor_model
        self.tiger_actor_model = tiger_actor_model
        self.placements_actor_model = placements_actor_model
        self.goat_citic_model = goat_citic_model
        self.tiger_critic_model = tiger_critic_model
        self.placement_critic_model = placement_critic_model


models = Models(
    goat_model.goat_actor_model,
    tiger_model.tiger_actor_model,
    goat_model.placement_actor_model,
    goat_model.goat_critic_model,
    tiger_model.tiger_critic_model,
    goat_model.placement_critic_model,
)
