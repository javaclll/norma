use crate::constants;
use crate::types::{
    GameStateInstance, GameStatus, GameStatusCheckResult, Move, MoveCheckResult, PossibleMove,
};
use crate::Baghchal;
use pyo3::prelude::*;
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

    pub fn state_as_inputs(&self, possible_moves_pre: Option<Vec<PossibleMove>>) -> Vec<Vec<i8>> {
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

            // Board positions
            for i in 0i8..5 {
                for j in 0i8..5 {
                    let piece = pos.board()[i as usize][j as usize];

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
            *self.move_reward_goat.last_mut().unwrap() += constants::G_GOAT_CAPTURED;
            *self.move_reward_tiger.last_mut().unwrap() += constants::T_GOAT_CAPTURE;
        }

        // Trapped tiger check
        if prev_trapped < self.trapped_tiger {
            *self.move_reward_goat.last_mut().unwrap() += constants::G_TIGER_TRAP;
            *self.move_reward_tiger.last_mut().unwrap() += constants::T_GOT_TRAPPED;
        } else if prev_trapped > self.trapped_tiger {
            *self.move_reward_goat.last_mut().unwrap() += constants::G_TIGER_ESCAPE;
            *self.move_reward_tiger.last_mut().unwrap() += constants::T_TRAP_ESCAPE;
        }

        // Has game been decided check
        let status_after_move = self.game_status_check();

        if status_after_move.decided {
            match status_after_move.won_by {
                -1 => {
                    self.game_state = GameStatus::TigerWon;
                    *self.move_reward_tiger.last_mut().unwrap() += constants::T_WIN;
                    *self.move_reward_goat.last_mut().unwrap() += constants::G_LOSE;
                }
                1 => {
                    self.game_state = GameStatus::GoatWon;
                    *self.move_reward_goat.last_mut().unwrap() += constants::G_WIN;
                    *self.move_reward_tiger.last_mut().unwrap() += constants::T_LOSE;
                }
                _ => {
                    self.game_state = GameStatus::Draw;
                    *self.move_reward_goat.last_mut().unwrap() += constants::G_DRAW;
                    *self.move_reward_tiger.last_mut().unwrap() += constants::T_DRAW;
                }
            }
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
        let mut b = BaghchalRS::default();
        b.load_game("XXA3-A5B5-XXA2-E1E2-XXA4-A1B1-XXA5-B1C2-XXA1-C2B1-XXB3-B1C2-XXB2-C2B1-XXB4-B5C4-XXB5-B1C2-XXC5-C2C1-XXD5-C1C2-XXB1-C2C1-XXE1-C1C2-XXC1-C2C3-XXC2-C3D2-XXC3".to_string());

        println!("{:?}", b.board()[0]);
        println!("{:?}", b.board()[1]);
        println!("{:?}", b.board()[2]);
        println!("{:?}", b.board()[3]);
        println!("{:?}", b.board()[4]);

        println!("{:?}", b.make_move_pgn("E2D1".to_string()));

        println!("{:?}", b.board()[0]);
        println!("{:?}", b.board()[1]);
        println!("{:?}", b.board()[2]);
        println!("{:?}", b.board()[3]);
        println!("{:?}", b.board()[4]);

        // println!("{:?}",b.make_move_pgn("D1C1".to_string()));
        //
        // println!("{:?}", b.board()[0]);
        // println!("{:?}", b.board()[1]);
        // println!("{:?}", b.board()[2]);
        // println!("{:?}", b.board()[3]);
        // println!("{:?}", b.board()[4]);
    }
}
