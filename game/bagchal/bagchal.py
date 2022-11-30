from copy import deepcopy

from .constant import DEFAULT_GAME_LAYOUT
from .enums import GameState
from .exception import GameException

# For Tiger
T_GOAT_CAPTURE = 4
T_GOT_TRAPPED = -2
T_TRAP_ESCAPE = 2
T_WIN = 5
T_LOSE = -5
T_DRAW = 0

# For Goat
G_GOAT_CAPTURED = -4
G_TIGER_TRAP = 5
G_TIGER_ESCAPE = -1
G_WIN = 10
G_LOSE = -10
G_DRAW = 0

# Max Moves
MAX_MOVES = 100


class Bagchal:
    def __init__(
        self,
        turn=0,
        goat_counter=0,
        goat_captured=0,
        game_state=GameState.NOT_DECIDED.value,
        game_history=[],
        pgn="",
        prev_move=None,
        move_reward_tiger=[],
        move_reward_goat=[],
        trapped_tiger=0,
    ):
        self.turn = turn
        self.goat_counter = goat_counter
        self.goat_captured = goat_captured
        self.game_state = game_state
        self.game_history = game_history
        self.pgn = pgn
        self.prev_move = prev_move
        self.move_reward_tiger = move_reward_tiger
        self.move_reward_goat = move_reward_goat
        self.trapped_tiger = trapped_tiger

    @property
    def board(self):
        return self.game_history[-1]["board"]

    @property
    def move_count(self):
        return len(self.game_history) - 1

    def pos_dec(self, num):
        if num == 1:
            return [1, 0, 0, 0, 0]
        elif num == 2:
            return [0, 1, 0, 0, 0]
        elif num == 3:
            return [0, 0, 1, 0, 0]
        elif num == 4:
            return [0, 0, 0, 1, 0]
        elif num == 5:
            return [0, 0, 0, 0, 1]

        return [0, 0, 0, 0, 0]

    def state_as_inputs(self, possible_moves=None):
        if not possible_moves:
            possible_moves = self.get_possible_moves()


        vector_list = []

        for neighbours in possible_moves:
            input = []

            pos = neighbours["resulting_state"]

            # Board Positions
            for i in range(5):
                for j in range(5):
                    if pos.board[i][j] == 1:
                        input += [1, 0]
                    elif pos.board[i][j] == -1:
                        input += [0, 1]
                    else:
                        input += [0, 0]

            coord = neighbours["move"]

            # Source
            input += self.pos_dec(coord[0][0])
            input += self.pos_dec(coord[0][1])

            # Destination
            input += self.pos_dec(coord[1][0])
            input += self.pos_dec(coord[1][1])

            # Goat Placement Complete
            if pos.goat_counter >= 20:
                input += [1]
            else:
                input += [0]

            # Goat or Tiger's Turn
            if self.turn == -1:
                input += [1]
            else:
                input += [0]

            vector_list.append(input)

        return vector_list

    @staticmethod
    def new():
        return Bagchal(
            goat_counter=0,
            goat_captured=0,
            turn=1,
            game_state=GameState.NOT_DECIDED.value,
            game_history=[
                {
                    "board": deepcopy(DEFAULT_GAME_LAYOUT),
                    "goat_count": 0,
                    "goat_captured": 0,
                }
            ],
            pgn="",
            prev_move=None,
            move_reward_tiger=[],
            move_reward_goat=[],
            trapped_tiger=0,
        )

    @staticmethod
    def cord_to_char(num):
        match (num):
            case 0:
                return "A"
            case 1:
                return "B"
            case 2:
                return "C"
            case 3:
                return "D"
            case 4:
                return "E"
            case _:
                return "X"

    @staticmethod
    def coord_to_png_unit(source, destination):
        unit = ""
        if source == None:
            unit = "XX"
        else:
            unit += Bagchal.cord_to_char(source[1])
            unit += str(5 - source[0])

        unit += Bagchal.cord_to_char(destination[1])
        unit += str(5 - destination[0])

        return unit

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
            source = [5 - int(pgn[1]), Bagchal.char_to_cord(pgn[0])]

        destination = [5 - int(pgn[3]), Bagchal.char_to_cord(pgn[2])]
        return (source, destination)

    def clear_game(self):
        self.goat_counter = 0
        self.goat_captured = 0
        self.game_state = GameState.NOT_DECIDED.value
        self.game_history = [
            {
                "board": deepcopy(DEFAULT_GAME_LAYOUT),
                "goat_count": 0,
                "goat_captured": 0,
            }
        ]
        self.turn = 1

    def load_game(self, pgn: str):
        self.clear_game()
        pgn = pgn.replace(" ", "").split("-")  # type: ignore

        for pgn_seg in pgn:
            source, target = self.pgn_unit_to_coord(pgn_seg)
            self.move(source, target)

    def resign(self, side):
        if side == 1:
            self.game_state = GameState.TIGER_WON.value

            return {
                "success": True,
                "won_by": -1,
            }
        elif side == -1:
            self.game_state = GameState.GOAT_WON.value
            return {
                "success": True,
                "won_by": 1,
            }
        else:
            raise GameException(message="Invalid parameter!")

    def check_trapped_tiger(self):
        count = 0
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == -1:
                    has_move = False

                    for k in range(5):
                        for l in range(5):
                            res = self.check_move([i, j], [k, l], assuming_turn=-1)
                            has_move = res["isValid"]
                            print(f"From: {i},{j} , To: {k},{l}, Result: {res}")
                            if has_move:
                                break
                        if has_move:
                            break

                    if not has_move:
                        count += 1

        self.trapped_tiger = count

    def move(self, source, target, eval_res=None):
        prev_captured = self.goat_captured
        prev_trapped = self.trapped_tiger

        if not eval_res:
            eval_res = self.check_move(source, target)

        if not eval_res["isValid"]:
            raise GameException(message="Invalid move!")

        self.move_reward_goat.append(0)
        self.move_reward_tiger.append(0)

        new_state = deepcopy(self.board)

        if eval_res.get("isPlaceMove"):
            new_state[target[0]][target[1]] = 1
            self.goat_counter += 1
        else:
            if eval_res["isCaptureMove"] == True:
                new_state[eval_res["capturePiece"][0]][eval_res["capturePiece"][1]] = 0
                self.goat_captured += 1

            new_state[source[0]][source[1]] = 0
            new_state[target[0]][target[1]] = self.turn

        self.turn = -1 if self.turn == 1 else 1

        self.game_history.append(
            {
                "board": new_state,
                "goat_count": self.goat_counter,
                "goat_captured": self.goat_captured,
            }
        )

        if self.pgn == "":
            self.pgn = Bagchal.coord_to_png_unit(source, target)
        else:
            self.pgn = self.pgn + "-" + Bagchal.coord_to_png_unit(source, target)  # type: ignore

        # self.check_trapped_tiger()

        self.prev_move = [source, target]

        # Goat got captured
        if prev_captured != self.goat_captured:
            self.move_reward_goat[-1] += G_GOAT_CAPTURED
            self.move_reward_tiger[-1] += T_GOAT_CAPTURE

        # Tiger got trapped
        if prev_trapped < self.trapped_tiger:
            self.move_reward_goat[-1] += G_TIGER_TRAP
            self.move_reward_tiger[-1] += T_GOT_TRAPPED

        # Tiger escaped trap
        if prev_trapped > self.trapped_tiger:
            self.move_reward_goat[-1] += G_TIGER_ESCAPE
            self.move_reward_tiger[-1] += T_TRAP_ESCAPE

        # Game has been decided
        status_after_move = self.game_status_check()

        if status_after_move["decided"]:
            if status_after_move["won_by"] == -1:
                self.game_state = GameState.TIGER_WON.value
                self.move_reward_tiger[-1] += T_WIN
                self.move_reward_goat[-1] += G_LOSE
            else:
                self.game_state = GameState.GOAT_WON.value
                self.move_reward_goat[-1] += G_WIN
                self.move_reward_tiger[-1] += T_LOSE

        # Max moves reached
        if len(self.game_history) >= MAX_MOVES:
            self.game_state = GameState.DRAW.value
            self.move_reward_goat[-1] += G_DRAW
            self.move_reward_tiger[-1] += T_DRAW

        return {"success": True}

    def check_move(self, source, target, assuming_turn = None):
        if assuming_turn:
            turn = assuming_turn
        else:
            turn = self.turn

        m = target[0]
        n = target[1]

        if source == None:
            if turn == 1:
                if self.goat_counter >= 20:
                    return {"isValid": False}
                else:
                    if self.board[m][n] != 0:
                        reason = "Target already has a piece!"
                        return {"isValid": False}
                    return {"isValid": True, "isPlaceMove": True}
            else:
                return {"isValid": False}

        x = source[0]
        y = source[1]

        position = self.board

        if x < 0 or y < 0 or m < 0 or n < 0 or x > 4 or y > 4 or m > 4 or n > 4:
            reason = "Cannot move outside the board!"
            # print(f'{reason} {x} {y} source {m} {n} destination {self.goat_counter}')
            return {"isValid": False, "reason": reason}

        if self.game_state != GameState.NOT_DECIDED.value:
            reason = "Cannot move after game has been decided!"
            # print(f'{reason} {x} {y} source {m} {n} destination {self.goat_counter}')
            return {"isValid": False, "reason": reason}

        if not (
            (turn == 1 and position[x][y] == 1)
            or (turn == -1 and position[x][y] == -1)
        ):
            reason = "Cannot move in other's turn!"
            # print(f'{reason} {x} {y} source {m} {n} destination {self.goat_counter}')
            return {"isValid": False, "reason": reason}

        if turn == 1:
            if self.goat_counter < 20:
                reason = "Can't move goat before all goats are placed"
                # print(f'{reason} {x} {y} source {m} {n} destination {self.goat_counter}')
                return {"isValid": False, "reason": reason}

        if position[m][n] != 0:
            reason = "Target already has a piece!"
            # print(f'{reason} {x} {y} source {m} {n} destination {self.goat_counter}')
            return {"isValid": False, "reason": reason}

        x_diff_abs = abs(x - m)
        y_diff_abs = abs(y - n)
        x_diff = m - x
        y_diff = n - y
        s_sum = x + y
        t_sum = m + n

        if x_diff_abs == 0 and y_diff_abs == 0:
            reason = "Source and target can't be same!"
            # print(f'{reason} {x} {y} source {m} {n} destination {self.goat_counter}')
            return {"isValid": False, "reason": reason}

        # Tiger can jump goats
        if (
            # (2,0), (2,2), (0, 2), (2, 2)
            turn == -1
            and (
                (x_diff_abs == 2 and y_diff_abs == 0)
                or (y_diff_abs == 2 and (x_diff_abs == 0 or x_diff_abs == 2))
            )
        ):
            if x_diff_abs == 2 and y_diff_abs == 2:
                if s_sum % 2 != 0:
                    reason = "Cannot jump diagonally from odd positions!"
                    # print(f'{reason} {x} {y} source {m} {n} destination {self.goat_counter}')
                    return {"isValid": False, "reason": reason}

            piece_to_capture = [int(x + x_diff / 2), int(y + y_diff / 2)]

            # Check if piece to capture is goat
            if position[piece_to_capture[0]][piece_to_capture[1]] == 1:
                reason = "Can capture goat!"
                # print(f'{reason} {x} {y} source {m} {n} destination {self.goat_counter}')
                return {
                    "isValid": True,
                    "isCaptureMove": True,
                    "capturePiece": piece_to_capture,
                    "reason": reason,
                }
            else:
                reason = "Cannot capture tiger!"
                # print(f'{reason} {x} {y} source {m} {n} destination {self.goat_counter}')
                return {"isValid": False, "reason": reason}

        # Can't move distance more than 2
        if x_diff_abs > 1 or y_diff_abs > 1:
            reason = "Cannot move distance more than 2!"
            # print(f'{reason} {x} {y} source {m} {n} destination {self.goat_counter}')
            return {"isValid": False, "reason": reason}
        # Can't move from odd position to another odd position
        # Example: 0,1 (0+1 = 1 odd) to 1,2 (1+2 = 3 odd)
        elif s_sum % 2:
            if t_sum % 2:
                reason = "Can't move from odd position to another odd position!"
                # print(f'{reason} {x} {y} source {m} {n} destination {self.goat_counter}')
                return {"isValid": False, "reason": reason}

        reason = "Default move!"
        # print(f'{reason} {x} {y} source {m} {n} destination {self.goat_counter}')
        return {"isValid": True, "reason": reason, "isCaptureMove": False}

    def tiger_can_move(self):
        position = self.board

        for i in range(5):
            for j in range(5):
                if position[i][j] == -1:
                    for k in range(5):
                        for l in range(5):
                            this_move = self.check_move([i, j], [k, l])
                            if this_move["isValid"]:
                                return True
        return False

    def goat_can_move(self):
        if self.goat_counter < 20 and self.turn == 1:
            return True

        position = self.board

        for i in range(5):
            for j in range(5):
                if position[i][j] == 1:
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            this_move = self.check_move([i, j], [i + k, j + l])
                            if this_move["isValid"]:
                                return True

    def game_status_check(self):
        if self.goat_captured >= 5:
            return {"decided": True, "won_by": -1}

        if self.turn == -1 and not self.tiger_can_move():
            return {"decided": True, "won_by": 1}
        elif self.turn == 1 and not self.goat_can_move():
            return {"decided": True, "won_by": -1}

        return {"decided": False}

    def get_possible_moves(self):
        moves = []

        if self.turn == -1:
            for i in range(5):
                for j in range(5):
                    if self.board[i][j] == -1:  # type: ignore
                        for k in range(-2, 3):
                            for l in range(-2, 3):
                                this_move = self.check_move([i, j], [i + k, j + l])
                                if this_move["isValid"]:
                                    new_move_state = deepcopy(self)
                                    new_move_state.move([i, j], [i + k, j + l], this_move)
                                    moves.append(  # type: ignore
                                        {
                                            "move": [[i, j], [i + k, j + l]],
                                            "resulting_state": new_move_state,
                                        }
                                    )
        else:
            if self.goat_counter >= 20:
                for i in range(5):
                    for j in range(5):
                        if self.board[i][j] == 1:  # type: ignore
                            for k in range(-1, 2):
                                for l in range(-1, 2):
                                    this_move = self.check_move([i, j], [i + k, j + l])
                                    if this_move["isValid"]:
                                        new_move_state = deepcopy(self)
                                        new_move_state.move(
                                            [i, j], [i + k, j + l], this_move
                                        )
                                        moves.append(  # type: ignore
                                            {
                                                "move": [[i, j], [i + k, j + l]],
                                                "resulting_state": new_move_state,
                                            }
                                        )
            else:
                for i in range(5):
                    for j in range(5):
                        if self.board[i][j] == 0:
                            new_move_state = deepcopy(self)
                            new_move_state.move(None, [i, j])

                            moves.append(
                                {
                                    "move": [None, [i, j]],
                                    "resulting_state": new_move_state,
                                }
                            )

        return moves
