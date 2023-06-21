use crate::{BaghchalRS, PossibleMove};
use crate::helpers::utils::*;
use rand::Rng;

impl BaghchalRS {
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

                board = rotate_matrix(board, no_of_rotations);
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
            input.append(&mut action_to_vector(move_.0, move_.1));

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

                board = rotate_matrix(board, no_of_rotations);
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
            input.append(&mut action_to_vector(move_.0, move_.1));

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

                board = rotate_matrix(board, no_of_rotations);
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
                action_to_vector_25(move_.0, move_.1);

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

                board = rotate_matrix(board, no_of_rotations);
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
            let action_repr = source_destination_repr_2d(move_.0, move_.1);

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

                board = rotate_matrix(board, no_of_rotations);
            }

            let move_ = neighbours.r#move;

            // Source and Destination
            let action_repr = source_destination_repr_2d(move_.0, move_.1);

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
            let (source_orig, dest_orig) = action_to_vector_25(move_.0, move_.1);

            let boards;
            if rotate_board {
                boards = get_transformed_boards(self.board(), source_orig, dest_orig)
                    .to_vec();
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
}
