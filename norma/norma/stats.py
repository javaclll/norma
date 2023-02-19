import json
from typing import List


class Stats:
    model_name: str
    game_counter: int
    positions_counter: int
    goat_trained_states: int
    tiger_trained_states: int

    goat_wins: int
    tiger_wins: int
    draws: int

    windows: List

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

        self.game_counter = 0
        self.positions_counter = 0
        self.goat_trained_states = 0
        self.tiger_trained_states = 0

        self.goat_wins = 0
        self.tiger_wins = 0
        self.draws = 0
        self.windows = []

        self.try_load()

    def save(self):
        try:
            stats_file = open(f"weights/{self.model_name}/training_stats.json", "w")
            json.dump(
                {
                    "game_counter": self.game_counter,
                    "positions_counter": self.positions_counter,
                    "goat_wins": self.goat_wins,
                    "tiger_wins": self.tiger_wins,
                    "draws": self.draws,
                    "goat_trained_states": self.goat_trained_states,
                    "tiger_trained_states": self.tiger_trained_states,
                    "windows": self.windows,
                },
                stats_file,
            )

        except Exception as e:
            print(f"{e}")

    def try_load(self):
        try:
            stats_file = open(f"weights/{self.model_name}/training_stats.json", "r")
            data = json.load(stats_file)

            self.game_counter = data["game_counter"]
            self.positions_counter = data["positions_counter"]
            self.goat_wins = data["goat_wins"]
            self.tiger_wins = data["tiger_wins"]
            self.draws = data["draws"]
            self.goat_trained_states = data["goat_trained_states"]
            self.tiger_trained_states = data["tiger_trained_states"]
            self.windows = data["windows"]

        except Exception as e:
            print(f"Didn't find stats file. Creating a new one!")

    def add(
        self,
        game_counter: int,
        positions_counter: int,
        goat_wins: int,
        tiger_wins: int,
        draws: int,
        goat_trained_states: int,
        tiger_trained_states: int,
        loss: float,
    ):
        self.game_counter += game_counter
        self.positions_counter += positions_counter
        self.goat_wins += goat_wins
        self.tiger_wins += tiger_wins
        self.draws += draws
        self.goat_trained_states += goat_trained_states
        self.tiger_trained_states += tiger_trained_states

        self.windows.append(
            {
                {
                    "game_counter": game_counter,
                    "positions_counter": positions_counter,
                    "goat_wins": goat_wins,
                    "tiger_wins": tiger_wins,
                    "draws": draws,
                    "goat_trained_states": goat_trained_states,
                    "tiger_trained_states": tiger_trained_states,
                    "loss": loss,
                },
            }
        )

    def print(self):
        print(f"---------------------------------------------------")
        print(f"OVERALL GAME STATS:")
        print(f"---------------------------------------------------")
        print(
            f"Goat: {self.goat_wins} ({((self.goat_wins/self.game_counter)*100):.2f} %)"
        )
        print(
            f"Tiger: {self.tiger_wins} ({((self.tiger_wins/self.game_counter)*100):.2f} %)"
        )
        print(f"Draws: {self.draws} ({((self.draws/self.game_counter)*100):.2f} %)")
        print(f"---------------------------------------------------")
        print(f"TRAINING STATS:")
        print(f"---------------------------------------------------")
        print(f"Games Played: {self.game_counter}")
        print(f"Positions Generated: {self.positions_counter}")
        print(f"Goat Trained States: {self.goat_trained_states}")
        print(f"Tiger Trained States: {self.tiger_trained_states}")
        print(f"Avg moves per game: {(self.positions_counter/self.game_counter):.2f}")

        cw_goat_wins = self.windows[-1]["goat_wins"]
        cw_tiger_wins = self.windows[-1]["tiger_wins"]
        cw_game_counter = self.windows[-1]["game_counter"]
        cw_draws = self.windows[-1]["draws"]
        print(f"---------------------------------------------------")
        print(f"CURRENT WINDOW GAME STATS:")
        print(f"---------------------------------------------------")
        print(f"Goat: {cw_goat_wins} ({((cw_goat_wins/cw_game_counter)*100):.2f} %)")
        print(f"Tiger: {cw_tiger_wins} ({((cw_tiger_wins/cw_game_counter)*100):.2f} %)")
        print(f"Draws: {cw_draws} ({((cw_draws/cw_game_counter)*100):.2f} %)")
