from enum import Enum


class GameState(Enum):
    NOT_DECIDED = 0
    GOAT_WON = 1
    TIGER_WON = 2
    DRAW = 3
