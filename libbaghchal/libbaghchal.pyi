from _typeshed import Self
from typing import Optional, List, Any, Tuple, Dict
import json


class Baghchal:
    def __new__(
        cls: type[Self],
        turn: Optional[int] = None,
        goat_counter: Optional[int] = None,
        goat_captured: Optional[int] = None,
        game_state: Optional[Any] = None,
        game_history: Optional[List[Any]] = None,
        pgn: Optional[str] = None,
        prev_move: Optional[Any] = None,
        move_reward_tiger: Optional[List[float]] = None,
        move_reward_goat: Optional[List[float]] = None,
        trapped_tiger: Optional[int] = None,
    ) -> Self:
        ...

    @staticmethod
    def default() -> Baghchal:
        ...

    @staticmethod
    def from_str(serialized: str) -> Baghchal:
        ...

    @staticmethod
    def pgn_unit_to_coord(pgn: str) -> Tuple[Optional[List[int]], List[int]]:
        ...

    @staticmethod
    def coord_to_png_unit(destination: List[int], source: Optional[List[int]]) -> str:
        ...

    def set_rewards(
        self,
        t_goat_capture,
        t_got_trapped,
        t_trap_escape,
        t_win,
        t_lose,
        t_draw,
        t_move,
        g_goat_captured,
        g_tiger_trap,
        g_tiger_escape,
        g_win,
        g_lose,
        g_draw,
        g_move,
    ):
        ...

    def copy(self) -> Baghchal:
        ...

    def to_str(self) -> str:
        ...

    def board(self) -> List[List[int]]:
        ...

    def move_count(self) -> int:
        ...

    def game_status_check(self) -> GameStatusCheckResult:
        ...

    def turn(self) -> int:
        ...

    def goat_counter(self) -> int:
        ...

    def goat_captured(self) -> int:
        ...

    def game_state(self) -> GameStatus:
        ...

    def game_history(self) -> List[GameStateInstance]:
        ...

    def pgn(self) -> str:
        ...

    def prev_move(self) -> Optional[Tuple[Optional[List[int]], List[int]]]:
        ...

    def move_reward_tiger(self) -> List[float]:
        ...

    def trapped_tiger(self) -> int:
        ...

    def move_reward_goat(self) -> List[float]:
        ...

    def state_as_inputs(
        self,
        possible_moves_pre: Optional[List[PossibleMove]],
        mode: Optional[int] = None,
        rotate_board: Optional[bool] = False,
    ) -> List[List[int]]:
        ...

    def clear_game(self) -> None:
        ...

    def resign(self, side) -> GameStatusCheckResult:
        ...

    def load_game(self, pgn: str) -> None:
        ...

    def make_move(
        self,
        target: List[int],
        source: Optional[List[int]],
        eval_res: Optional[MoveCheckResult],
    ):
        ...

    def get_possible_moves(self) -> List[PossibleMove]:
        ...


class GameStatus:
    NotDecided: Any
    GoatWon: Any
    TigerWon: Any
    Draw: Any

    def to_value(self) -> int:
        ...

    @staticmethod
    def from_value(value: int) -> GameStatus:
        ...


class PossibleMove:
    move: Tuple[Optional[List[int]], List[int]]
    resulting_state: Baghchal

    def to_str(self) -> str:
        ...


class MoveCheckResult:
    is_valid: bool
    is_place_move: bool
    is_capture_move: bool
    capture_piece: Optional[List[int]]
    reason: str

    def to_str(self) -> str:
        ...


class GameStatusCheckResult:
    decided: bool
    won_by: int

    def to_str(self) -> str:
        ...


class GameStateInstance:
    board: List[List[int]]
    goat_count: int
    goat_captured: int

    def to_str(self) -> str:
        ...
