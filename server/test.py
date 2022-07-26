
import uuid
from typing import List, Optional
from core.enums import GameState, MessageTypes


DEFAULT_GAME_LAYOUT = [
    [-1, 0, 0, 0, -1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [-1, 0, 0, 0, -1],
]


class Game:
    def __init__(
        self,
        game_id,
        tiger,
        goat,
        goat_counter,
        goat_captured,
        game_state,
        game_history,
        turn,
        socket,
    ):
        self.game_id = game_id
        self.tiger = tiger
        self.goat = goat
        self.goat_counter = goat_counter
        self.goat_captured = goat_captured
        self.game_state = game_state
        self.game_history = game_history
        self.turn = turn
        self.socket = socket

    @staticmethod
    def new():
        return Game(
            game_id=uuid.uuid4(),
            tiger=None,
            goat=None,
            goat_counter=0,
            goat_captured=0,
            game_state=GameState.NOT_DECIDED.value,
            game_history=[DEFAULT_GAME_LAYOUT.copy()],
            turn=1,
            socket=[],
        )

    @staticmethod
    def char_to_cord(char):
        match (char):
            case "A":
                return 0
            case "B":
                return 1
            case "C":
                return 2
            case "D":
                return 3
            case "E":
                return 4

    @staticmethod
    def pgn_unit_to_coord(pgn):
        if pgn[0:2] == "XX":
            source = None
        else:
            source = [5 - int(pgn[1]), Game.char_to_cord(pgn[0])]

        destination = [5 - int(pgn[3]), Game.char_to_cord(pgn[2])]
        return (source, destination)

    def clear_game(self):
        self.goat_counter = 0
        self.goat_captured = 0
        self.game_state = GameState.NOT_DECIDED.value
        self.game_history = [DEFAULT_GAME_LAYOUT.copy()]
        self.turn = 1

    def load_game(self, pgn: str):
        self.clear_game()
        pgn = pgn.replace(" ", "").split("-")  # type: ignore

        for pgn_seg in pgn:
            source, target = self.pgn_unit_to_coord(pgn_seg)
            self.move(source, target, ident_check=False)

    def resign(self, ident):
        if ident == self.goat:
            self.game_state = GameState.TIGER_WON.value

            return {
                "success": True,
                "won_by": -1,
            }
        elif ident == self.tiger:
            self.game_state = GameState.GOAT_WON.value
            return {
                "success": True,
                "won_by": 1,
            }
        else:
            return {
                "success": False,
                "reason": "Unauthorized user!",
            }

    def move(self, source, target, ident=None, ident_check=True):
        if ident_check:
            if self.tiger == ident:
                ident_piece = -1
            elif self.goat == ident:
                ident_piece = 1
            else:
                return {
                    "success": False,
                    "reason": "Unauthorized user!",
                }

            if ident_piece != self.turn:
                return {
                    "success": False,
                    "reason": "Not the players turn!",
                }

        eval_move = self.check_move(source, target)

        if not eval_move["isValid"]:
            return {"success": False, "reason": "Invalid move!"}

        new_state = self.game_history[-1].copy()

        if eval_move.get("isPlaceMove"):
            new_state[target[0]][target[1]] = 1
        else:
            if eval_move["isCaptureMove"] == True:
                new_state[eval_move["capturePiece"][0]][
                    eval_move["capturePiece"][1]
                ] = 0
                self.goat_captured += 1

            new_state[source[0]][source[1]] = 0
            new_state[target[0]][target[1]] = self.turn

        self.turn = -1 if self.turn == 1 else 1

        self.game_history.append(new_state)

        return {"success": True}

    def check_move(self, source, target):
        if source == None and self.turn == 1:
            if self.goat_counter >= 20:
                return {"isValid": False}
            else:
                return {"isValid": True, "isPlaceMove": True}

        x = source[0]
        y = source[1]
        m = target[0]
        n = target[1]

        position = self.game_history[-1]

        if x < 0 or y < 0 or m < 0 or n < 0 or x > 4 or y > 4 or m > 4 or n > 4:
            reason = "Cannot move outside the board!"
            print(reason)
            return {"isValid": False, "reason": reason}

        if self.game_state != GameState.NOT_DECIDED.value:
            reason = "Cannot move after game has been decided!"
            print(reason)
            return {"isValid": False, "reason": reason}

        if not (
            (self.turn == 1 and position[x][y] == 1)
            or (self.turn == -1 and position[x][y] == -1)
        ):
            reason = "Cannot move in other's turn!"
            print(reason)
            return {"isValid": False, "reason": reason}

        if self.turn == 1:
            if self.goat_counter < 20:
                reason = "Can't move goat before all goats are placed"
                print(reason)
                return {"isValid": False, "reason": reason}

        if position[m][n] != 0:
            reason = "Target already has a piece!"
            print(reason)
            return {"isValid": False, "reason": reason}

        x_diff_abs = abs(x - m)
        y_diff_abs = abs(y - n)
        x_diff = m - x
        y_diff = n - y
        s_sum = x + y
        t_sum = m + n

        if x_diff_abs == 0 and y_diff_abs == 0:
            reason = "Source and target can't be same!"
            print(reason)
            return {"isValid": False, "reason": reason}

        # Tiger can jump goats
        if (
            # (2,0), (2,2), (0, 2), (2, 2)
            self.turn == -1
            and (
                (x_diff_abs == 2 and y_diff_abs == 0)
                or (y_diff_abs == 2 and (x_diff_abs == 0 or x_diff_abs == 2))
            )
        ):
            if x_diff_abs == 2 and y_diff_abs == 2:
                if s_sum % 2 != 0:
                    reason = "Cannot jump diagonally from odd positions!"
                    print(reason)
                    return {"isValid": False, "reason": reason}

            piece_to_capture = [int(x + x_diff / 2), int(y + y_diff / 2)]

            # Check if piece to capture is goat
            if position[piece_to_capture[0]][piece_to_capture[1]] == 1:
                reason = "Can capture goat!"
                print(reason)
                return {
                    "isValid": True,
                    "isCaptureMove": True,
                    "capturePiece": piece_to_capture,
                    "reason": reason,
                }
            else:
                reason = "Cannot capture tiger!"
                print(reason)
                return {"isValid": False, "reason": reason}

        # Can't move distance more than 2
        if x_diff_abs > 1 or y_diff_abs > 1:
            reason = "Cannot move distance more than 2!"
            print(reason)
            return {"isValid": False, "reason": reason}
        # Can't move from odd position to another odd position
        # Example: 0,1 (0+1 = 1 odd) to 1,2 (1+2 = 3 odd)
        elif s_sum % 2:
            if t_sum % 2:
                reason = "Can't move from odd position to another odd position!"
                print(reason)
                return {"isValid": False, "reason": reason}

        reason = "Default move!"
        return {"isValid": True, "reason": reason, "isCaptureMove": False}

    def tiger_can_move(self):
        position = self.game_history[-1]

        for i in range(5):
            for j in range(5):
                if position[i][j] == -1:
                    for k in range(-2, 3):
                        for l in range(-2, 3):
                            this_move = self.check_move([i, j], [i + k, j + l])
                            if this_move["isValid"]:
                                return True
        return False

    def goat_can_move(self):
        if self.goat_counter < 20 and self.turn == 1:
            return True

        position = self.game_history[-1]

        for i in range(5):
            for j in range(5):
                if position[i][j] == 1:
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            this_move = self.check_move([i, j], [i + k, j + l])
                            if this_move["isValid"]:
                                return True

    def game_status_check(self):
        if self.goat_captured >= 6:
            return {"decided": True, "wonBy": -1}

        if self.turn == -1 and not self.tiger_can_move():
            return {"decided": True, "wonBy": 1}
        elif self.turn == 1 and not self.goat_can_move():
            return {"decided": True, "wonBy": -1}

        return {"decided": False}
