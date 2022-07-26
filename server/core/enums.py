from enum import Enum


class GameState(Enum):
    NOT_DECIDED = 0
    GOAT_WON = 1
    TIGER_WON = 2


class MessageTypes(Enum):
    GoatWinByResign = 1
    TigerWinByResign = 2
    TigerWins = 3
    GoatWins = 4
    Notification = 5
    ResignBroadcast = 6
