use crate::types::{
    GameStateInstance, GameStatus, GameStatusCheckResult, Move, MoveCheckResult, PossibleMove,
};
use crate::Baghchal;
use pyo3::prelude::*;
use rand::Rng;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct BaghchalRS {
    pub turn: i8,
    pub goat_counter: i8,
    pub goat_captured: i8,
    pub game_state: GameStatus,
    pub game_history: Vec<GameStateInstance>,
    pub pgn: String,
    pub prev_move: Option<Move>,
    pub move_reward_tiger: Vec<f32>,
    pub move_reward_goat: Vec<f32>,
    pub trapped_tiger: i8,

    // For tiger
    pub t_goat_capture: f32,
    pub t_got_trapped: f32,
    pub t_trap_escape: f32,
    pub t_win: f32,
    pub t_lose: f32,
    pub t_draw: f32,
    pub t_move: f32,

    // For Goat
    pub g_goat_captured: f32,
    pub g_tiger_trap: f32,
    pub g_tiger_escape: f32,
    pub g_win: f32,
    pub g_lose: f32,
    pub g_draw: f32,
    pub g_move: f32,
}

impl Default for BaghchalRS {
    fn default() -> Self {
        Self {
            turn: 1,
            goat_counter: 0,
            goat_captured: 0,
            game_state: GameStatus::NotDecided,
            game_history: [GameStateInstance::default()].to_vec(),
            pgn: "".to_string(),
            prev_move: None,
            move_reward_tiger: [].to_vec(),
            move_reward_goat: [].to_vec(),
            trapped_tiger: 0,
            t_goat_capture: 0.0,
            t_got_trapped: 0.0,
            t_trap_escape: 0.0,
            t_win: 0.0,
            t_lose: 0.0,
            t_draw: 0.0,
            t_move: 0.0,
            g_goat_captured: 0.0,
            g_tiger_trap: 0.0,
            g_tiger_escape: 0.0,
            g_win: 0.0,
            g_lose: 0.0,
            g_draw: 0.0,
            g_move: 0.0,
        }
    }
}

impl Into<Baghchal> for BaghchalRS {
    fn into(self) -> Baghchal {
        Baghchal { inner: self }
    }
}

impl BaghchalRS {
    pub fn board(&self) -> [[i8; 5]; 5] {
        return self.game_history.last().unwrap().board;
    }

    pub fn move_count(&self) -> i8 {
        return (self.game_history.len() - 1) as i8;
    }

    pub fn set_rewards(
        &mut self,
        t_goat_capture: f32,
        t_got_trapped: f32,
        t_trap_escape: f32,
        t_win: f32,
        t_lose: f32,
        t_draw: f32,
        t_move: f32,
        g_goat_captured: f32,
        g_tiger_trap: f32,
        g_tiger_escape: f32,
        g_win: f32,
        g_lose: f32,
        g_draw: f32,
        g_move: f32,
    ) {
        self.t_goat_capture = t_goat_capture;
        self.t_got_trapped = t_got_trapped;
        self.t_trap_escape = t_trap_escape;
        self.t_win = t_win;
        self.t_lose = t_lose;
        self.t_draw = t_draw;
        self.t_move = t_move;
        self.g_goat_captured = g_goat_captured;
        self.g_tiger_trap = g_tiger_trap;
        self.g_tiger_escape = g_tiger_escape;
        self.g_win = g_win;
        self.g_lose = g_lose;
        self.g_draw = g_draw;
        self.g_move = g_move;
    }

    pub fn cord_to_char(num: i8) -> char {
        match num {
            0 => return 'A',
            1 => return 'B',
            2 => return 'C',
            3 => return 'D',
            4 => return 'E',
            _ => return 'X',
        }
    }

    pub fn char_to_cord(c: char) -> i8 {
        match c {
            'A' => return 0,
            'B' => return 1,
            'C' => return 2,
            'D' => return 3,
            'E' => return 4,
            _ => return -1,
        }
    }

    pub fn pos_dec(num: i8) -> Vec<i8> {
        match num {
            1 => return [1, 0, 0, 0, 0].to_vec(),
            2 => return [0, 1, 0, 0, 0].to_vec(),
            3 => return [0, 0, 1, 0, 0].to_vec(),
            4 => return [0, 0, 0, 1, 0].to_vec(),
            5 => return [0, 0, 0, 0, 1].to_vec(),
            _ => return [0, 0, 0, 0, 0].to_vec(),
        }
    }

    fn rotate_matrix(matrix: [[i8; 5]; 5]) -> [[i8; 5]; 5] {
        let mut mat: [[i8; 5]; 5] = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ];

        for i in 0..5 {
            for j in 0..5 {
                mat[j][4 - i] = matrix[i][j];
            }
        }

        return mat;
    }

    pub fn action_to_vector(source: Option<[i8; 2]>, destination: [i8; 2]) -> Vec<i8> {
        let mut vector = Vec::<i8>::with_capacity(20);

        if source.is_none() {
            vector.append(&mut [0, 0, 0, 0, 0, 0, 0, 0, 0, 0].to_vec());
        } else {
            vector.append(&mut BaghchalRS::pos_dec(source.unwrap()[0]));
            vector.append(&mut BaghchalRS::pos_dec(source.unwrap()[1]));
        }

        vector.append(&mut BaghchalRS::pos_dec(destination[0]));
        vector.append(&mut BaghchalRS::pos_dec(destination[1]));

        return vector;
    }

    pub fn action_to_vector_25(
        source: Option<[i8; 2]>,
        destination: [i8; 2],
    ) -> ([[i8; 5]; 5], [[i8; 5]; 5]) {
        let mut vector = (
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
        );

        // Source
        match source {
            Some(value) => {
                let s1 = value[0] as usize;
                let s2 = value[1] as usize;
                vector.0[s1][s2] = 1;
            }
            None => {}
        }

        // Destination
        let d1 = destination[0] as usize;
        let d2 = destination[1] as usize;
        vector.1[d1][d2] = 1;

        return vector;
    }

    /*
     * Board Positions: 25 * 2 bits per postion = 50
     * Source : 5 in X dirn and 5 in Y dirn = 10
     * Destination : 5 in X dirn and 5 in Y dirn = 10
     * Goat Placement Complete : 1
     * Turn : 1
     * -----------------------------------------------
     * Total : 72
     */
    pub fn state_as_inputs_mode_1(
        &self,
        possible_moves_pre: Option<Vec<PossibleMove>>,
        rotate_board: Option<bool>,
    ) -> Vec<Vec<i8>> {
        let possible_moves: Vec<PossibleMove>;

        if possible_moves_pre.is_none() {
            possible_moves = self.get_possible_moves();
        } else {
            possible_moves = possible_moves_pre.unwrap();
        }

        let mut vector_list = Vec::<Vec<i8>>::new();

        for neighbours in possible_moves {
            let pos = neighbours.resulting_state;
            let mut input = Vec::<i8>::new();

            let mut board = self.board();

            if rotate_board == Some(true) {
                let no_of_rotations = rand::thread_rng().gen_range(0..4);

                for _ in 0..no_of_rotations {
                    board = Self::rotate_matrix(board);
                }
            }

            // Board positions
            for i in 0i8..5 {
                for j in 0i8..5 {
                    let piece = board[i as usize][j as usize];

                    match piece {
                        1 => {
                            input.push(1);
                            input.push(0);
                        }
                        -1 => {
                            input.push(0);
                            input.push(1);
                        }
                        _ => {
                            input.push(0);
                            input.push(0);
                        }
                    }
                }
            }

            let move_ = neighbours.r#move;

            // Source and Destination
            input.append(&mut BaghchalRS::action_to_vector(move_.0, move_.1));

            // Goat placement complete
            if pos.goat_counter() >= 20 {
                input.push(1)
            } else {
                input.push(0)
            };

            // Goat or tiger's turn
            if self.turn == -1 {
                input.push(1)
            } else {
                input.push(0)
            };

            vector_list.push(input);
        }

        return vector_list;
    }

    /*
     *  Board: 25 position = 25 + 15 padders = 40
     *  Source: 5 in X dirn and 5 in y dirn  = 10
     *  Destination: 5 in X dirn and 5 in y dirn  = 10
     *  Goat Placement Complete: 1
     *  Turn: 1
     *  Padder: 2
     *  ---------------------------------------------------
     *  Total: 64 : 8*8
     */
    pub fn state_as_inputs_mode_2(
        &self,
        possible_moves_pre: Option<Vec<PossibleMove>>,
        rotate_board: Option<bool>,
    ) -> Vec<Vec<i8>> {
        let possible_moves: Vec<PossibleMove>;

        if possible_moves_pre.is_none() {
            possible_moves = self.get_possible_moves();
        } else {
            possible_moves = possible_moves_pre.unwrap();
        }

        let mut vector_list = Vec::<Vec<i8>>::new();

        for neighbours in possible_moves {
            let pos = neighbours.resulting_state;
            let mut input = Vec::<i8>::new();

            let mut board = self.board();

            if rotate_board == Some(true) {
                let no_of_rotations = rand::thread_rng().gen_range(0..4);

                for _ in 0..no_of_rotations {
                    board = Self::rotate_matrix(board);
                }
            }

            // Goat positions
            for i in 0i8..5 {
                for j in 0i8..5 {
                    let piece = board[i as usize][j as usize];

                    match piece {
                        1 => {
                            input.push(1);
                        }
                        -1 => {
                            input.push(-1);
                        }
                        _ => {
                            input.push(0);
                        }
                    }
                }
                input.push(0);
                input.push(0);
                input.push(0);
            }

            let move_ = neighbours.r#move;

            // Source and Destination
            input.append(&mut BaghchalRS::action_to_vector(move_.0, move_.1));

            // Goat placement complete
            if pos.goat_counter() >= 20 {
                input.push(1)
            } else {
                input.push(0)
            };

            // Goat or tiger's turn
            if self.turn == -1 {
                input.push(1)
            } else {
                input.push(0)
            };

            // Padders
            input.push(0);
            input.push(0);

            vector_list.push(input);
        }

        return vector_list;
    }

    /*
     *  Board: 25 position = 25
     *  Source: 5 in X dirn and 5 in y dirn  = 25
     *  Destination: 5 in X dirn and 5 in y dirn  = 25
     *  Goat Placement Complete: 1
     *  Goats Captured: 4
     *  Padder: 20
     *  ---------------------------------------------------
     *  Total: 100 : 10 * 10
     */
    pub fn state_as_inputs_mode_3(
        &self,
        possible_moves_pre: Option<Vec<PossibleMove>>,
        rotate_board: Option<bool>,
    ) -> Vec<Vec<i8>> {
        let possible_moves: Vec<PossibleMove>;

        if possible_moves_pre.is_none() {
            possible_moves = self.get_possible_moves();
        } else {
            possible_moves = possible_moves_pre.unwrap();
        }

        let mut vector_list = Vec::<[[i8; 10]; 10]>::new();

        for neighbours in possible_moves {
            let pos = neighbours.resulting_state;
            let mut input = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ];

            let mut board = self.board();

            if rotate_board == Some(true) {
                let no_of_rotations = rand::thread_rng().gen_range(0..4);

                for _ in 0..no_of_rotations {
                    board = Self::rotate_matrix(board);
                }
            }

            // Board Positions
            for i in 0i8..5 {
                for j in 0i8..5 {
                    input[i as usize][j as usize] = board[i as usize][j as usize];
                }
            }

            let move_ = neighbours.r#move;

            // Source and Destination
            let (source_array, destination_array) =
                BaghchalRS::action_to_vector_25(move_.0, move_.1);

            for i in 0i8..5 {
                for j in 0i8..5 {
                    input[i as usize][5 + j as usize] = source_array[i as usize][j as usize];
                }
            }

            for i in 0i8..5 {
                for j in 0i8..5 {
                    input[5 + i as usize][j as usize] = destination_array[i as usize][j as usize];
                }
            }

            // Goat placement complete
            if pos.goat_counter() >= 20 {
                input[5][5] = 1;
            };

            // Number of goats captured
            match pos.goat_captured() {
                1 => {
                    input[5][6] = 1;
                }

                2 => {
                    input[5][6] = 1;
                    input[5][7] = 1;
                }

                3 => {
                    input[5][6] = 1;
                    input[5][7] = 1;
                    input[5][8] = 1;
                }

                4 => {
                    input[5][6] = 1;
                    input[5][7] = 1;
                    input[5][8] = 1;
                    input[5][9] = 1;
                }
                _ => {}
            }
            vector_list.push(input);
        }

        return vector_list
            .iter()
            .map(|item| item.iter().flatten().cloned().collect::<Vec<i8>>())
            .collect();
    }

    pub fn state_as_inputs(
        &self,
        possible_moves_pre: Option<Vec<PossibleMove>>,
        mode: Option<i8>,
        rotate_board: Option<bool>,
    ) -> Vec<Vec<i8>> {
        match mode {
            Some(1) => return self.state_as_inputs_mode_1(possible_moves_pre, rotate_board),
            Some(2) => return self.state_as_inputs_mode_2(possible_moves_pre, rotate_board),
            Some(3) => return self.state_as_inputs_mode_3(possible_moves_pre, rotate_board),
            _ => return self.state_as_inputs_mode_1(possible_moves_pre, rotate_board),
        }
    }

    pub fn pgn_unit_to_coord(pgn: String) -> Move {
        let source: Option<[i8; 2]>;

        let pgn_iter = pgn.chars().collect::<Vec<char>>();

        if *pgn_iter.get(1).unwrap() == 'X' {
            source = None;
        } else {
            source = Some([
                5 - pgn_iter.get(1).unwrap().to_digit(10).unwrap() as i8,
                BaghchalRS::char_to_cord(*pgn_iter.get(0).unwrap()),
            ]);
        }

        let destination = [
            5 - pgn_iter.get(3).unwrap().to_digit(10).unwrap() as i8,
            BaghchalRS::char_to_cord(*pgn_iter.get(2).unwrap()),
        ];

        return (source, destination);
    }

    pub fn coord_to_png_unit(source: Option<[i8; 2]>, destination: [i8; 2]) -> String {
        let mut unit = String::new();

        // Source coordinates to PGN
        if source.is_none() {
            unit = "XX".to_string();
        } else {
            unit.push(BaghchalRS::cord_to_char(source.unwrap()[1]));
            unit.push_str(&(5 - source.unwrap()[0]).to_string());
        };

        // Destination coordinates to PGN
        unit.push(BaghchalRS::cord_to_char(destination[1]));
        unit.push_str(&(5 - destination[0]).to_string());

        return unit;
    }

    pub fn clear_game(&mut self) {
        self.goat_counter = 0;
        self.goat_captured = 0;
        self.game_state = GameStatus::NotDecided;
        self.game_history = [GameStateInstance::default()].to_vec();
        self.turn = 1;
    }

    pub fn resign(&mut self, side: i8) -> GameStatusCheckResult {
        if side == 1 {
            self.game_state = GameStatus::TigerWon;

            return GameStatusCheckResult {
                decided: true,
                won_by: -1,
            };
        } else if side == -1 {
            self.game_state = GameStatus::GoatWon;

            return GameStatusCheckResult {
                decided: true,
                won_by: 1,
            };
        } else {
            return GameStatusCheckResult {
                decided: false,
                won_by: 0,
            };
        }
    }

    pub fn load_game(&mut self, pgn: String) {
        self.clear_game();
        let compact_pgn = pgn.replace(" ", "");
        let pgn_units: Vec<&str> = compact_pgn.split("-").collect();

        for pgn_seg in pgn_units {
            let (source, target) = BaghchalRS::pgn_unit_to_coord(pgn_seg.to_string());
            self.make_move(source, target, None);
        }
    }

    pub fn check_trapped_tiger(&mut self) {
        let mut count = 0;

        for i in 0i8..5 {
            for j in 0i8..5 {
                let board = self.board();
                if board[i as usize][j as usize] == -1 {
                    let mut has_move = false;

                    for k in 0i8..5 {
                        for l in 0i8..5 {
                            let res = self.check_move(Some([i, j]), [k, l], None);
                            has_move = res.is_valid;
                            if has_move {
                                break;
                            }
                        }
                        if has_move {
                            break;
                        };
                    }

                    if !has_move {
                        count += 1;
                    }
                }
            }
        }

        self.trapped_tiger = count;
    }

    pub fn make_move_pgn(&mut self, pgn: String) -> MoveCheckResult {
        let (source, target) = BaghchalRS::pgn_unit_to_coord(pgn);
        return self.make_move(source, target, None);
    }

    pub fn make_move(
        &mut self,
        source: Option<[i8; 2]>,
        target: [i8; 2],
        eval_res: Option<MoveCheckResult>,
    ) -> MoveCheckResult {
        let prev_captured = self.goat_captured;
        let prev_trapped = self.trapped_tiger;

        let move_eval: MoveCheckResult;
        if eval_res.is_none() {
            move_eval = self.check_move(source, target, None);
        } else {
            move_eval = eval_res.unwrap();
        }

        if !move_eval.is_valid {
            return move_eval;
        }

        self.move_reward_goat.push(0f32);
        self.move_reward_tiger.push(0f32);

        let mut new_state = self.board().clone();

        if move_eval.is_place_move {
            new_state[target[0usize] as usize][target[1usize] as usize] = 1;
            self.goat_counter += 1;
        } else {
            if move_eval.is_capture_move {
                let piece = move_eval.capture_piece.unwrap();
                new_state[piece[0] as usize][piece[1] as usize] = 0;
                self.goat_captured += 1;
            }

            new_state[source.unwrap()[0usize] as usize][source.unwrap()[1usize] as usize] = 0;
            new_state[target[0usize] as usize][target[1usize] as usize] = self.turn;
        }

        // Change the turn
        self.turn = if self.turn == -1 { 1 } else { -1 };

        // Push to game history
        self.game_history.push(GameStateInstance {
            board: new_state,
            goat_count: self.goat_counter,
            goat_captured: self.goat_captured,
        });

        // Append PGN unit after move
        if self.pgn == "" {
            self.pgn = BaghchalRS::coord_to_png_unit(source, target);
        } else {
            self.pgn.push('-');
            self.pgn
                .push_str(&BaghchalRS::coord_to_png_unit(source, target));
        }

        self.prev_move = Some((source, target));

        // Goats captured check
        if prev_captured != self.goat_captured {
            *self.move_reward_goat.last_mut().unwrap() += self.g_goat_captured;
            *self.move_reward_tiger.last_mut().unwrap() += self.t_goat_capture;
        }

        // Trapped tiger check
        if prev_trapped < self.trapped_tiger {
            *self.move_reward_goat.last_mut().unwrap() += self.g_tiger_trap;
            *self.move_reward_tiger.last_mut().unwrap() += self.t_got_trapped;
        } else if prev_trapped > self.trapped_tiger {
            *self.move_reward_goat.last_mut().unwrap() += self.g_tiger_escape;
            *self.move_reward_tiger.last_mut().unwrap() += self.t_trap_escape;
        }

        // Has game been decided check
        let status_after_move = self.game_status_check();

        if status_after_move.decided {
            match status_after_move.won_by {
                -1 => {
                    self.game_state = GameStatus::TigerWon;
                    *self.move_reward_tiger.last_mut().unwrap() += self.t_win;
                    *self.move_reward_goat.last_mut().unwrap() += self.g_lose;
                }
                1 => {
                    self.game_state = GameStatus::GoatWon;
                    *self.move_reward_goat.last_mut().unwrap() += self.g_win;
                    *self.move_reward_tiger.last_mut().unwrap() += self.t_lose;
                }
                _ => {
                    self.game_state = GameStatus::Draw;
                    *self.move_reward_goat.last_mut().unwrap() += self.g_draw;
                    *self.move_reward_tiger.last_mut().unwrap() += self.t_draw;
                }
            }
        }

        // Move Cost
        // Note: turn is already changed so inverted
        if self.turn == -1 {
            *self.move_reward_goat.last_mut().unwrap() += self.g_move;
        } else {
            *self.move_reward_tiger.last_mut().unwrap() += self.t_move;
        }

        return move_eval;
    }

    pub fn check_move(
        &self,
        source: Option<[i8; 2]>,
        target: [i8; 2],
        assuming_turn: Option<i8>,
    ) -> MoveCheckResult {
        let turn: i8;

        if assuming_turn.is_some() {
            turn = assuming_turn.unwrap();
        } else {
            turn = self.turn;
        }

        let m = target[0] as i8;
        let n = target[1] as i8;

        let position = self.board();

        // Place Move Check
        if source.is_none() {
            // If turn is of goat
            if turn == 1 {
                // If all goats have been placed
                if self.goat_counter >= 20 {
                    return MoveCheckResult {
                        is_valid: false,
                        reason: "Cannot place any more goats!".to_string(),
                        ..Default::default()
                    };
                }
                // If all goats haven't been placed
                else {
                    // If target position already has a piece
                    if position[m as usize][n as usize] != 0 {
                        return MoveCheckResult {
                            is_valid: false,
                            reason: "Target already has a piece!".to_string(),
                            ..Default::default()
                        };
                    }
                    // If target doesn't have a piece
                    else {
                        return MoveCheckResult {
                            is_valid: true,
                            reason: "Goat place move!".to_string(),
                            is_place_move: true,
                            ..Default::default()
                        };
                    }
                }
            }
            // If turn is of tiger
            else {
                return MoveCheckResult {
                    is_valid: false,
                    reason: "Tiger can't place!".to_string(),
                    ..Default::default()
                };
            }
        }

        let x = source.unwrap()[0] as i8;
        let y = source.unwrap()[1] as i8;

        // Board boundary check
        if x < 0 || y < 0 || m < 0 || n < 0 || x > 4 || y > 4 || m > 4 || n > 4 {
            return MoveCheckResult {
                is_valid: false,
                reason: "Cannot move outside the board!".to_string(),
                ..Default::default()
            };
        }

        // Game state check
        if self.game_state != GameStatus::NotDecided {
            return MoveCheckResult {
                is_valid: false,
                reason: "Cannot move after game has been decided!".to_string(),
                ..Default::default()
            };
        }

        // Turn check
        if !((turn == 1 && position[x as usize][y as usize] == 1)
            || (turn == -1 && position[x as usize][y as usize] == -1))
        {
            return MoveCheckResult {
                is_valid: false,
                reason: "Cannot move in other's turn!".to_string(),
                ..Default::default()
            };
        }

        // Goat can't move before placing all goats
        if turn == 1 && self.goat_counter < 20 {
            return MoveCheckResult {
                is_valid: false,
                reason: "Cannot move goat before all goats are placed".to_string(),
                ..Default::default()
            };
        }

        // Target already has a piece check
        if position[m as usize][n as usize] != 0 {
            return MoveCheckResult {
                is_valid: false,
                reason: "Target already has a piece!".to_string(),
                ..Default::default()
            };
        }

        let x_diff_abs = x.abs_diff(m) as usize;
        let y_diff_abs = y.abs_diff(n) as usize;
        let s_sum = x + y;
        let t_sum = m + n;

        // Source and target check
        if x_diff_abs == 0 && y_diff_abs == 0 {
            return MoveCheckResult {
                is_valid: false,
                reason: "Source and target can't be same!".to_string(),
                ..Default::default()
            };
        }

        // Tiger jump over goat check
        if turn == -1 {
            let can_jump = match (x_diff_abs, y_diff_abs) {
                // Can only move diagonally from even position
                (2, 2) => s_sum % 2 == 0,

                // Horizontal jump move possible on all positions
                (2, 0) => true,

                // Vertical jump move possible on all positions
                (0, 2) => true,

                // Distance 1 move possible on all positions
                (1, 0) => return MoveCheckResult::default(),

                // Can only jump diagonally from even position
                (1, 1) => {
                    if s_sum % 2 == 0 {
                        return MoveCheckResult::default();
                    } else {
                        return MoveCheckResult {
                            is_valid: false,
                            reason: "Cannot move diagonally from odd positions".to_string(),
                            ..Default::default()
                        };
                    }
                }

                // Distance 1 move possible on all positions
                (0, 1) => return MoveCheckResult::default(),
                _ => false,
            };

            if !can_jump {
                return MoveCheckResult {
                    is_valid: false,
                    reason: "Requested jump move is invalid!".to_string(),
                    ..Default::default()
                };
            }

            let piece_to_capture = [((x + m) / 2) as i8, ((y + n) / 2) as i8];

            // If capture piece is goat
            if position[piece_to_capture[0] as usize][piece_to_capture[1] as usize] == 1 {
                return MoveCheckResult {
                    is_valid: true,
                    is_capture_move: true,
                    capture_piece: Some(piece_to_capture),
                    reason: "Can capture goat!".to_string(),
                    ..Default::default()
                };
            } else {
                return MoveCheckResult {
                    is_valid: false,
                    reason: "Cannot capture tiger or empty space!".to_string(),
                    ..Default::default()
                };
            }
        }

        // Cannot move distance more than 2 check
        if x_diff_abs > 1 || y_diff_abs > 1 {
            return MoveCheckResult {
                is_valid: false,
                reason: "Cannot move distance more than 2!".to_string(),
                ..Default::default()
            };
        }
        // Odd to Odd position check
        else if s_sum % 2 != 0 && t_sum % 2 != 0 {
            return MoveCheckResult {
                is_valid: false,
                reason: "Cannot move from odd position to another odd position!".to_string(),
                ..Default::default()
            };
        }

        return MoveCheckResult::default();
    }

    pub fn goat_can_move(&self) -> bool {
        if self.goat_counter < 20 && self.turn == 1 {
            return true;
        }

        let position = self.board();

        for i in 0i8..5 {
            for j in 0i8..5 {
                if position[i as usize][j as usize] == 1 {
                    for k in -1i8..2 {
                        for l in -1i8..2 {
                            let this_move = self.check_move(Some([i, j]), [i + k, j + l], None);
                            if this_move.is_valid {
                                return true;
                            }
                        }
                    }
                }
            }
        }
        false
    }

    pub fn tiger_can_move(&self) -> bool {
        let position = self.board();

        for i in 0i8..5 {
            for j in 0i8..5 {
                if position[i as usize][j as usize] == -1 {
                    for k in 0i8..5 {
                        for l in 0i8..5 {
                            let this_move = self.check_move(Some([i, j]), [k, l], None);
                            if this_move.is_valid {
                                return true;
                            }
                        }
                    }
                }
            }
        }
        false
    }

    pub fn game_status_check(&self) -> GameStatusCheckResult {
        if self.goat_captured >= 5 {
            return GameStatusCheckResult {
                decided: true,
                won_by: -1,
            };
        } else if self.turn == -1 && !self.tiger_can_move() {
            return GameStatusCheckResult {
                decided: true,
                won_by: 1,
            };
        } else if self.turn == 1 && !self.goat_can_move() {
            return GameStatusCheckResult {
                decided: true,
                won_by: -1,
            };
        } else if self.move_count() >= 100 {
            return GameStatusCheckResult {
                decided: true,
                won_by: 0,
            };
        } else {
            return GameStatusCheckResult {
                decided: false,
                won_by: -1,
            };
        }
    }

    pub fn get_possible_moves(&self) -> Vec<PossibleMove> {
        let mut moves = Vec::<PossibleMove>::new();

        let position = self.board();

        if self.turn == -1 {
            for i in 0i8..5 {
                for j in 0i8..5 {
                    if position[i as usize][j as usize] == -1 {
                        for k in 0i8..5 {
                            for l in 0i8..5 {
                                let this_move = self.check_move(Some([i, j]), [k, l], None);
                                if this_move.is_valid {
                                    let mut new_move_state = self.clone();
                                    new_move_state.make_move(Some([i, j]), [k, l], None);
                                    moves.push(PossibleMove {
                                        r#move: (Some([i, j]), [k, l]),
                                        resulting_state: new_move_state.into(),
                                    });
                                }
                            }
                        }
                    }
                }
            }
        } else if self.goat_counter >= 20 {
            for i in 0i8..5 {
                for j in 0i8..5 {
                    if position[i as usize][j as usize] == 1 {
                        for k in -1i8..2 {
                            for l in -1i8..2 {
                                let this_move = self.check_move(Some([i, j]), [i + k, j + l], None);
                                if this_move.is_valid {
                                    let mut new_move_state = self.clone();
                                    new_move_state.make_move(Some([i, j]), [i + k, j + l], None);
                                    moves.push(PossibleMove {
                                        r#move: (Some([i, j]), [i + k, j + l]),
                                        resulting_state: new_move_state.into(),
                                    });
                                }
                            }
                        }
                    }
                }
            }
        } else {
            for i in 0i8..5 {
                for j in 0i8..5 {
                    if position[i as usize][j as usize] == 0 {
                        let mut new_move_state = self.clone();
                        new_move_state.make_move(None, [i, j], None);
                        moves.push(PossibleMove {
                            r#move: (None, [i, j]),
                            resulting_state: new_move_state.into(),
                        });
                    }
                }
            }
        }
        return moves;
    }
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_default() {
        let mut test = BaghchalRS::default();
        test.make_move_pgn("XXA3".to_string());
        test.make_move_pgn("A1A2".to_string());
        test.make_move_pgn("XXA4".to_string());
        test.make_move_pgn("A5B5".to_string());
        test.make_move_pgn("XXA5".to_string());
        test.make_move_pgn("B5C5".to_string());
        test.make_move_pgn("XXA1".to_string());

        let a = [
            [1, 0, -1, 0, -1, 0, 0, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, -1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ];

        println!("{:?}", test.state_as_inputs_mode_3(None, Some(false))[0]);
    }
}
