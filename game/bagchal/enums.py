from enum import Enum

class AgentType(Enum):
    GOAT = 1
    TIGER = -1

class GameState(Enum):
    NOT_DECIDED = 0
    GOAT_WON = 1
    TIGER_WON = 2
    DRAW = 3
