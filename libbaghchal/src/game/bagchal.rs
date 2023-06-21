use crate::helpers::types::*;
use crate::helpers::utils::*;
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
    pub transition_history: Vec<TransitionHistoryInstance>,
    pub pgn: String,
    pub prev_move: Option<Move>,
    pub move_reward_tiger: Vec<f32>,
    pub move_reward_goat: Vec<f32>,
    pub trapped_tiger: i8,
    pub game_over_on_invalid: bool,

    // For tiger
    pub t_goat_capture: Option<f32>,
    pub t_got_trapped: Option<f32>,
    pub t_trap_escape: Option<f32>,
    pub t_win: Option<f32>,
    pub t_lose: Option<f32>,
    pub t_draw: Option<f32>,
    pub t_move: Option<f32>,

    // For Goat
    pub g_goat_captured: Option<f32>,
    pub g_tiger_trap: Option<f32>,
    pub g_tiger_escape: Option<f32>,
    pub g_win: Option<f32>,
    pub g_lose: Option<f32>,
    pub g_draw: Option<f32>,
    pub g_move: Option<f32>,

    // Common
    pub gt_invalid_move: Option<f32>,
}

impl Default for BaghchalRS {
    fn default() -> Self {
        Self {
            turn: 1,
            goat_counter: 0,
            goat_captured: 0,
            game_state: GameStatus::NotDecided,
            game_history: [GameStateInstance::default()].to_vec(),
            transition_history: [].to_vec(),
            pgn: "".to_string(),
            game_over_on_invalid: false,
            prev_move: None,
            move_reward_tiger: [].to_vec(),
            move_reward_goat: [].to_vec(),
            trapped_tiger: 0,
            t_goat_capture: Some(0.0),
            t_got_trapped: Some(0.0),
            t_trap_escape: Some(0.0),
            t_win: Some(0.0),
            t_lose: Some(0.0),
            t_draw: Some(0.0),
            t_move: Some(0.0),
            g_goat_captured: Some(0.0),
            g_tiger_trap: Some(0.0),
            g_tiger_escape: Some(0.0),
            g_win: Some(0.0),
            g_lose: Some(0.0),
            g_draw: Some(0.0),
            g_move: Some(0.0),
            gt_invalid_move: Some(0.0),
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

    pub fn set_game_over_on_invalid(&mut self, state: bool) {
        self.game_over_on_invalid = state;
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
        gt_invalid_move: f32,
    ) {
        self.t_goat_capture = Some(t_goat_capture);
        self.t_got_trapped = Some(t_got_trapped);
        self.t_trap_escape = Some(t_trap_escape);
        self.t_win = Some(t_win);
        self.t_lose = Some(t_lose);
        self.t_draw = Some(t_draw);
        self.t_move = Some(t_move);
        self.g_goat_captured = Some(g_goat_captured);
        self.g_tiger_trap = Some(g_tiger_trap);
        self.g_tiger_escape = Some(g_tiger_escape);
        self.g_win = Some(g_win);
        self.g_lose = Some(g_lose);
        self.g_draw = Some(g_draw);
        self.g_move = Some(g_move);
        self.gt_invalid_move = Some(gt_invalid_move);
    }

    pub fn state_as_inputs_all_symmetry(
        &self,
        possible_moves_pre: Option<Vec<PossibleMove>>,
    ) -> Vec<Vec<Vec<i8>>> {
        // Tiger Map (25) = [
        //      1, 0, 0, 0, 1,
        //      0, 0, 0, 0, 0,
        //      0, 0, 0, 0, 0,
        //      0, 0, 0, 1, 0,
        //      1, 0, 0, 0, 0,
        // ]
        //
        // Goat Map (25) = [
        //      0, 0, 0, 1, 0,
        //      1, 0, 0, 0, 0,
        //      1, 1, 1, 0, 1,
        //      0, 0, 0, 0, 1,
        //      0, 1, 0, 1 0,
        // ]
        //
        // Blank map (25) = [
        //      0, 1, 1, 0, 0,
        //      0, 0, 0, 0, 1,
        //      0, 0, 0, 0, 0,
        //      0, 0, 0, 0, 1,
        //      0, 0, 0, 01 0,
        // ]
        //
        // Destination map (25) = [
        //      0, 1, 1, 0, 0,
        //      0, 0, 0, 0, 1,
        //      0, 0, 0, 0, 0,
        //      0, 0, 0, 0, 1,
        //      0, 0, 0, 01 0,
        // ]
        //
        // Source map (25) = [
        //      0, 1, 1, 0, 0,
        //      0, 0, 0, 0, 1,
        //      0, 0, 0, 0, 0,
        //      0, 0, 0, 0, 1,
        //      0, 0, 0, 01 0,
        // ]
        //
        // Goat Placement Complete: 1
        // Goats Captured: 4
        // Turn: 1
        // ---------------------------------------------------------------
        // Total: 131

        let possible_moves: Vec<PossibleMove>;

        if possible_moves_pre.is_none() {
            possible_moves = self.get_possible_moves();
        } else {
            possible_moves = possible_moves_pre.unwrap();
        }

        let mut vector_list = Vec::<Vec<Vec<i8>>>::new();

        for neighbours in possible_moves {
            let vecs = self.coord_to_input(neighbours.r#move.0, neighbours.r#move.1, true);
            vector_list.push(vecs);
        }

        return vector_list;
    }

    pub fn coord_to_input(
        &self,
        source: Option<[i8; 2]>,
        destination: [i8; 2],
        rotate_board: bool,
    ) -> Vec<Vec<i8>> {
        let mut vector_list = Vec::<Vec<i8>>::new();

        // Source and Destination
        let (source_orig, dest_orig) = action_to_vector_25(source, destination);

        let boards;
        if rotate_board {
            boards = get_transformed_boards(self.board(), source_orig, dest_orig).into();
        } else {
            boards = [(self.board(), source_orig, dest_orig)].to_vec();
        }

        for (board, source_map, destination_map) in boards {
            let mut vector_map: Vec<i8> = vec![0; 131];

            // Board Positions
            for i in 0usize..5 {
                for j in 0usize..5 {
                    match board[i as usize][j as usize] {
                        1 => vector_map[i * 5 + j] = 1,
                        -1 => vector_map[25 + i * 5 + j] = 1,
                        _ => vector_map[50 + i * 5 + j] = 1,
                    };
                }
            }

            for i in 0usize..25 {
                vector_map[75 + i] = source_map[i / 5][i % 5];
                vector_map[100 + i] = destination_map[i / 5][i % 5];
            }

            // Goat placement complete
            if self.goat_counter >= 20 {
                vector_map[125] = 1;
            };

            // Number of goats captured
            if self.goat_captured != 0 {
                vector_map[126 + self.goat_captured as usize - 1] = 1;
            }

            // Turn
            if self.turn == -1 {
                vector_map[130] = 1;
            }

            vector_list.push(vector_map.to_vec());
        }

        return vector_list;
    }

    pub fn index_to_input(&self, index: usize, symmetry: i8) -> Vec<Vec<i8>> {
        let move_: Move;
        if self.turn == -1 {
            move_ = Self::i2m_tiger(index);
        } else if self.turn == 1 && self.goat_counter < 20 {
            move_ = Self::i2m_placement(index);
        } else {
            move_ = Self::i2m_goat(index);
        }

        let (source_map, dest_map) = action_to_vector_25(move_.0, move_.1);

        let (normal_source_map, normal_dest_map) = undo_symmetry(source_map, dest_map, symmetry);

        let (normal_source, normal_dest) =
            vector_25_to_action((normal_source_map, normal_dest_map));

        return self.coord_to_input(normal_source, normal_dest, true);
    }

    pub fn state_as_inputs(
        &self,
        possible_moves_pre: Option<Vec<PossibleMove>>,
        mode: Option<i8>,
        rotate_board: Option<bool>,
    ) -> Vec<Vec<i8>> {
        match mode {
            Some(1) => return self.state_as_inputs_mode_1(possible_moves_pre, rotate_board, false),
            Some(2) => return self.state_as_inputs_mode_2(possible_moves_pre, rotate_board, false),
            Some(3) => return self.state_as_inputs_mode_3(possible_moves_pre, rotate_board, false),
            Some(4) => return self.state_as_inputs_mode_4(possible_moves_pre, rotate_board, false),
            Some(5) => return self.state_as_inputs_mode_5(possible_moves_pre, rotate_board, false),
            Some(6) => {
                return self.state_as_inputs_mode_6(
                    possible_moves_pre,
                    rotate_board.unwrap_or(false),
                    false,
                )
            }
            _ => panic!("Invalid inputs mode!"),
        }
    }

    pub fn states_all_symmetry(
        &self,
        possible_moves_pre: Option<Vec<PossibleMove>>,
    ) -> Vec<Vec<Vec<i8>>> {
        return self.state_as_inputs_all_symmetry(possible_moves_pre);
    }

    pub fn state_as_input_actor(
        &self,
        possible_moves_pre: Option<Vec<PossibleMove>>,
        mode: Option<i8>,
        rotate_board: Option<bool>,
    ) -> Vec<Vec<i8>> {
        let state = match mode {
            Some(1) => self.state_as_inputs_mode_1(possible_moves_pre, rotate_board, true),
            Some(2) => self.state_as_inputs_mode_2(possible_moves_pre, rotate_board, true),
            Some(3) => self.state_as_inputs_mode_3(possible_moves_pre, rotate_board, true),
            Some(4) => self.state_as_inputs_mode_4(possible_moves_pre, rotate_board, true),
            Some(5) => self.state_as_inputs_mode_5(possible_moves_pre, rotate_board, true),
            Some(6) => {
                self.state_as_inputs_mode_6(possible_moves_pre, rotate_board.unwrap_or(true), true)
            }
            _ => panic!("Invalid inputs mode!"),
        };

        return state;
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
            let (source, target) = pgn_unit_to_coord(pgn_seg.to_string());
            self.make_move(source, target, None, true);
        }
    }
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_default() {
        // let (source, dest) = (None, [2, 1]);

        let mut bag = BaghchalRS::default();
        bag.make_move(Some([2, 1]), [2, 2], None, true);

        println!("{:?}", bag.states_all_symmetry(None)[0]);
    }
}
