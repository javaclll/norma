from enum import Enum


class MessageTypes(Enum):
    GoatWinByResign = 1
    TigerWinByResign = 2
    TigerWins = 3
    GoatWins = 4
    Notification = 5
    ResignBroadcast = 6
