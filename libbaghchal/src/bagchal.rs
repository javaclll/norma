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

    fn rotate_matrix(matrix: [[i8; 5]; 5], times: i8) -> [[i8; 5]; 5] {
        let mut ret_board = matrix;

        for _ in 0..times {
            let mut mat: [[i8; 5]; 5] = [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ];

            for i in 0..5 {
                for j in 0..5 {
                    mat[j][4 - i] = ret_board[i][j];
                }
            }

            ret_board = mat;
        }

        return ret_board;
    }

    fn y_reflect_matrix(matrix: [[i8; 5]; 5]) -> [[i8; 5]; 5] {
        let mut mat: [[i8; 5]; 5] = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ];

        for i in 0..5 {
            for j in 0..5 {
                mat[i][4 - j] = matrix[i][j];
            }
        }

        return mat;
    }

    fn x_reflect_matrix(matrix: [[i8; 5]; 5]) -> [[i8; 5]; 5] {
        let mut mat: [[i8; 5]; 5] = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ];

        for i in 0..5 {
            for j in 0..5 {
                mat[4 - i][j] = matrix[i][j];
            }
        }

        return mat;
    }

    fn origin_reflect_matrix(matrix: [[i8; 5]; 5]) -> [[i8; 5]; 5] {
        let mut mat: [[i8; 5]; 5] = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ];

        for i in 0..5 {
            for j in 0..5 {
                mat[j][i] = matrix[i][j];
            }
        }

        return mat;
    }

    fn get_transformed_boards(
        matrix: [[i8; 5]; 5],
        source_map: [[i8; 5]; 5],
        destination_map: [[i8; 5]; 5],
    ) -> [([[i8; 5]; 5], [[i8; 5]; 5], [[i8; 5]; 5]); 7] {
        return [
            (matrix, source_map, destination_map),
            (
                Self::rotate_matrix(matrix, 1),
                Self::rotate_matrix(source_map, 1),
                Self::rotate_matrix(destination_map, 1),
            ),
            (
                Self::rotate_matrix(matrix, 2),
                Self::rotate_matrix(source_map, 2),
                Self::rotate_matrix(destination_map, 2),
            ),
            (
                Self::rotate_matrix(matrix, 3),
                Self::rotate_matrix(source_map, 3),
                Self::rotate_matrix(destination_map, 3),
            ),
            (
                Self::x_reflect_matrix(matrix),
                Self::x_reflect_matrix(source_map),
                Self::x_reflect_matrix(destination_map),
            ),
            (
                Self::y_reflect_matrix(matrix),
                Self::y_reflect_matrix(source_map),
                Self::y_reflect_matrix(destination_map),
            ),
            (
                Self::origin_reflect_matrix(matrix),
                Self::origin_reflect_matrix(source_map),
                Self::origin_reflect_matrix(destination_map),
            ),
        ];
    }

    fn undo_symmetry(
        source_map: [[i8; 5]; 5],
        dest_map: [[i8; 5]; 5],
        symmetry: i8,
    ) -> ([[i8; 5]; 5], [[i8; 5]; 5]) {
        match symmetry {
            0 => return (source_map, dest_map),
            1 => {
                return (
                    Self::rotate_matrix(source_map, 3),
                    Self::rotate_matrix(dest_map, 3),
                )
            }
            2 => {
                return (
                    Self::rotate_matrix(source_map, 2),
                    Self::rotate_matrix(dest_map, 2),
                )
            }
            3 => {
                return (
                    Self::rotate_matrix(source_map, 1),
                    Self::rotate_matrix(dest_map, 1),
                )
            }
            4 => {
                return (
                    Self::x_reflect_matrix(source_map),
                    Self::x_reflect_matrix(dest_map),
                )
            }
            5 => {
                return (
                    Self::y_reflect_matrix(source_map),
                    Self::y_reflect_matrix(dest_map),
                )
            }
            6 => {
                return (
                    Self::origin_reflect_matrix(source_map),
                    Self::origin_reflect_matrix(dest_map),
                )
            }
            _ => panic!("Invalid symmetry!"),
        };
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

    pub fn source_destination_repr_2d(
        source: Option<[i8; 2]>,
        destination: [i8; 2],
    ) -> [[[i8; 2]; 5]; 5] {
        let mut vector = [
            [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
            [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
        ];

        // Source
        match source {
            Some(value) => {
                let s1 = value[0] as usize;
                let s2 = value[1] as usize;
                vector[s1][s2][0] = 1;
            }
            None => {}
        }

        // Destination
        let d1 = destination[0] as usize;
        let d2 = destination[1] as usize;
        vector[d1][d2][1] = 1;

        return vector;
    }

    pub fn vector_25_to_action(vector: ([[i8; 5]; 5], [[i8; 5]; 5])) -> Move {
        let source_vector = vector.0;
        let dest_vector = vector.1;

        let mut source: Option<[i8; 2]> = None;
        let mut dest: Option<[i8; 2]> = None;

        for i in 0..5i8 {
            for j in 0..5i8 {
                if source_vector[i as usize][j as usize] == 1 {
                    source = Some([i, j])
                }
                if dest_vector[i as usize][j as usize] == 1 {
                    dest = Some([i, j])
                }
            }
        }

        return (source, dest.expect("Dest can't be `None`!"));
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
        one: bool,
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

                board = Self::rotate_matrix(board, no_of_rotations);
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

            if one {
                return vector_list;
            }
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
        one: bool,
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

                board = Self::rotate_matrix(board, no_of_rotations);
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

            if one {
                return vector_list;
            }
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
        one: bool,
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

                board = Self::rotate_matrix(board, no_of_rotations);
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

            if one {
                return vector_list
                    .iter()
                    .map(|item| item.iter().flatten().cloned().collect::<Vec<i8>>())
                    .collect();
            }
        }

        return vector_list
            .iter()
            .map(|item| item.iter().flatten().cloned().collect::<Vec<i8>>())
            .collect();
    }

    pub fn state_as_inputs_mode_4(
        &self,
        possible_moves_pre: Option<Vec<PossibleMove>>,
        rotate_board: Option<bool>,
        one: bool,
    ) -> Vec<Vec<i8>> {
        // Board Map (75) = [
        //     [0,0,1], [0,0,1], [0,0,1], [0,0,1], [0,0,1],
        //     [0,0,1], [0,0,1], [0,0,1], [0,0,1], [0,0,1],
        //     [0,0,1], [0,0,1], [0,0,1], [0,0,1], [0,0,1],
        //     [0,0,1], [0,0,1], [0,0,1], [0,0,1], [0,0,1],
        //     [0,0,1], [0,0,1], [0,0,1], [0,0,1], [0,0,1],
        // ]
        //
        // Source Destination Map (50) = [
        //  [0,0], [0,0], [0,0], [0,0], [0,0],
        //  [0,0], [1,0], [0,0], [0,0], [0,0],
        //  [0,0], [0,0], [0,1], [0,0], [0,0],
        //  [0,0], [0,0], [0,0], [0,0], [0,0],
        //  [0,0], [0,0], [0,0], [0,0], [0,0],
        // ]
        //
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

        let mut vector_list = Vec::<Vec<i8>>::new();

        for neighbours in possible_moves {
            let pos = neighbours.resulting_state;
            let mut input = Vec::<i8>::new();

            let mut board = self.board();

            if rotate_board == Some(true) {
                let no_of_rotations = rand::thread_rng().gen_range(0..4);

                board = Self::rotate_matrix(board, no_of_rotations);
            }

            // Board Positions
            for i in 0i8..5 {
                for j in 0i8..5 {
                    match board[i as usize][j as usize] {
                        1 => input.append(&mut vec![1, 0, 0]),
                        -1 => input.append(&mut vec![0, 1, 0]),
                        _ => input.append(&mut vec![0, 0, 1]),
                    }
                }
            }

            let move_ = neighbours.r#move;

            // Source and Destination
            let action_repr = BaghchalRS::source_destination_repr_2d(move_.0, move_.1);

            for i in 0i8..5 {
                for j in 0i8..5 {
                    input.append(&mut action_repr[i as usize][j as usize].to_vec());
                }
            }

            // Goat placement complete
            if pos.goat_counter() >= 20 {
                input.push(1);
            } else {
                input.push(0);
            };

            // Number of goats captured
            match pos.goat_captured() {
                1 => input.append(&mut [1, 0, 0, 0].to_vec()),
                2 => input.append(&mut [0, 1, 0, 0].to_vec()),
                3 => input.append(&mut [0, 0, 1, 0].to_vec()),
                4 => input.append(&mut [0, 0, 0, 1].to_vec()),
                _ => input.append(&mut [0, 0, 0, 0].to_vec()),
            }

            // Turn
            if pos.turn() == -1 {
                input.push(1);
            } else {
                input.push(0);
            };

            vector_list.push(input);

            if one {
                return vector_list;
            }
        }

        return vector_list;
    }

    pub fn state_as_inputs_mode_5(
        &self,
        possible_moves_pre: Option<Vec<PossibleMove>>,
        rotate_board: Option<bool>,
        one: bool,
    ) -> Vec<Vec<i8>> {
        // Board Map (125) = [
        //     [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0],
        //     [0,0,1,0,0], [0,0,1,1,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0],
        //     [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,1], [0,0,1,0,0], [0,0,1,0,0],
        //     [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0],
        //     [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0], [0,0,1,0,0],
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

        let mut vector_list = Vec::<Vec<i8>>::new();

        for neighbours in possible_moves {
            let pos = neighbours.resulting_state;
            let mut input = Vec::<i8>::new();

            let mut board = self.board();

            if rotate_board == Some(true) {
                let no_of_rotations = rand::thread_rng().gen_range(0..4);

                board = Self::rotate_matrix(board, no_of_rotations);
            }

            let move_ = neighbours.r#move;

            // Source and Destination
            let action_repr = BaghchalRS::source_destination_repr_2d(move_.0, move_.1);

            // Board Positions
            for i in 0i8..5 {
                for j in 0i8..5 {
                    match board[i as usize][j as usize] {
                        1 => input.append(&mut vec![1, 0, 0]),
                        -1 => input.append(&mut vec![0, 1, 0]),
                        _ => input.append(&mut vec![0, 0, 1]),
                    };

                    input.append(&mut action_repr[i as usize][j as usize].to_vec());
                }
            }

            // Goat placement complete
            if pos.goat_counter() >= 20 {
                input.push(1);
            } else {
                input.push(0);
            };

            // Number of goats captured
            match pos.goat_captured() {
                1 => input.append(&mut [1, 0, 0, 0].to_vec()),
                2 => input.append(&mut [0, 1, 0, 0].to_vec()),
                3 => input.append(&mut [0, 0, 1, 0].to_vec()),
                4 => input.append(&mut [0, 0, 0, 1].to_vec()),
                _ => input.append(&mut [0, 0, 0, 0].to_vec()),
            }

            // Turn
            if pos.turn() == -1 {
                input.push(1);
            } else {
                input.push(0);
            };

            vector_list.push(input);

            if one {
                return vector_list;
            }
        }

        return vector_list;
    }
    pub fn state_as_inputs_mode_6_old(
        &self,
        possible_moves_pre: Option<Vec<PossibleMove>>,
        rotate_board: bool,
    ) -> Vec<Vec<i8>> {
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

        let mut vector_list = Vec::<Vec<i8>>::new();

        for neighbours in possible_moves {
            let move_ = neighbours.r#move;

            // Source and Destination
            let (source_orig, dest_orig) = BaghchalRS::action_to_vector_25(move_.0, move_.1);

            let boards;
            if rotate_board {
                boards =
                    Self::get_transformed_boards(self.board(), source_orig, dest_orig).to_vec();
            } else {
                boards = [(self.board(), source_orig, dest_orig)].to_vec();
            }

            for (board, source_map, destination_map) in boards {
                let mut vector_map: [i8; 131] = [0; 131];

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
        }

        return vector_list;
    }

    pub fn state_as_inputs_mode_6(
        &self,
        possible_moves_pre: Option<Vec<PossibleMove>>,
        rotate_board: bool,
        one: bool,
    ) -> Vec<Vec<i8>> {
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

        let mut vector_list = Vec::<Vec<i8>>::new();

        for neighbours in possible_moves {
            let mut vecs =
                self.coord_to_input(neighbours.r#move.0, neighbours.r#move.1, rotate_board);
            vector_list.append(&mut vecs);

            if one {
                return vector_list;
            }
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
        let (source_orig, dest_orig) = BaghchalRS::action_to_vector_25(source, destination);

        let boards;
        if rotate_board {
            boards = Self::get_transformed_boards(self.board(), source_orig, dest_orig).to_vec();
        } else {
            boards = [(self.board(), source_orig, dest_orig)].to_vec();
        }

        for (board, source_map, destination_map) in boards {
            let mut vector_map: [i8; 131] = [0; 131];

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

        let (source_map, dest_map) = Self::action_to_vector_25(move_.0, move_.1);

        let (normal_source_map, normal_dest_map) =
            Self::undo_symmetry(source_map, dest_map, symmetry);

        let (normal_source, normal_dest) =
            Self::vector_25_to_action((normal_source_map, normal_dest_map));

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

    pub fn make_move_with_symmetry(
        &mut self,
        source: Option<[i8; 2]>,
        target: [i8; 2],
        symmetry: i8,
    ) -> MoveCheckResult {
        let (source_map, dest_map) = Self::action_to_vector_25(source, target);

        let (normal_source_map, normal_dest_map) =
            Self::undo_symmetry(source_map, dest_map, symmetry);

        let (normal_source, normal_dest) =
            Self::vector_25_to_action((normal_source_map, normal_dest_map));

        return self.make_move(normal_source, normal_dest, None);
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
            *self.move_reward_goat.last_mut().unwrap() += self.g_goat_captured.unwrap();
            *self.move_reward_tiger.last_mut().unwrap() += self.t_goat_capture.unwrap();
        }

        // Trapped tiger check
        if prev_trapped < self.trapped_tiger {
            *self.move_reward_goat.last_mut().unwrap() += self.g_tiger_trap.unwrap();
            *self.move_reward_tiger.last_mut().unwrap() += self.t_got_trapped.unwrap();
        } else if prev_trapped > self.trapped_tiger {
            *self.move_reward_goat.last_mut().unwrap() += self.g_tiger_escape.unwrap();
            *self.move_reward_tiger.last_mut().unwrap() += self.t_trap_escape.unwrap();
        }

        // Has game been decided check
        let status_after_move = self.game_status_check();

        if status_after_move.decided {
            match status_after_move.won_by {
                -1 => {
                    self.game_state = GameStatus::TigerWon;
                    *self.move_reward_tiger.last_mut().unwrap() += self.t_win.unwrap();
                    *self.move_reward_goat.last_mut().unwrap() += self.g_lose.unwrap();
                }
                1 => {
                    self.game_state = GameStatus::GoatWon;
                    *self.move_reward_goat.last_mut().unwrap() += self.g_win.unwrap();
                    *self.move_reward_tiger.last_mut().unwrap() += self.t_lose.unwrap();
                }
                _ => {
                    self.game_state = GameStatus::Draw;
                    *self.move_reward_goat.last_mut().unwrap() += self.g_draw.unwrap();
                    *self.move_reward_tiger.last_mut().unwrap() += self.t_draw.unwrap();
                }
            }
        }

        // Move Cost
        // Note: turn is already changed so inverted
        if self.turn == -1 {
            *self.move_reward_goat.last_mut().unwrap() += self.g_move.unwrap();
        } else {
            *self.move_reward_tiger.last_mut().unwrap() += self.t_move.unwrap();
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
        // let mut test = [
        //     [-1, 0, 1, 0, -1],
        //     [0, 0, 0, 0, 0],
        //     [0, 0, 0, 0, 0],
        //     [0, 0, 0, 0, 0],
        //     [-1, 0, 0, 0, -1],
        // ];

        let (source, dest) = (None, [2, 1]);

        assert_eq!(
            (source, dest),
            BaghchalRS::vector_25_to_action(BaghchalRS::action_to_vector_25(source, dest))
        );

        // println!(
        //     "{:?}",
        //     BaghchalRS::vector_25_to_action(BaghchalRS::action_to_vector_25(source, dest)),
        // );
    }
}
