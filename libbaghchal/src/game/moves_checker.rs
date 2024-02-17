use crate::helpers::types::*;
use crate::helpers::utils::*;
use crate::{BaghchalRS, PossibleMove};

impl BaghchalRS {
    pub fn make_move_pgn(&mut self, pgn: String) -> MoveCheckResult {
        let (source, target) = crate::helpers::utils::pgn_unit_to_coord(pgn);
        return self.make_move(source, target, None, true);
    }

    pub fn make_move_with_symmetry(
        &mut self,
        source: Option<[i8; 2]>,
        target: [i8; 2],
        symmetry: i8,
    ) -> MoveCheckResult {
        let (source_map, dest_map) = action_to_vector_25(source, target);

        let (normal_source_map, normal_dest_map) = undo_symmetry(source_map, dest_map, symmetry);

        let (normal_source, normal_dest) =
            vector_25_to_action((normal_source_map, normal_dest_map));

        return self.make_move(normal_source, normal_dest, None, true);
    }

    pub fn make_move(
        &mut self,
        source: Option<[i8; 2]>,
        target: [i8; 2],
        eval_res: Option<MoveCheckResult>,
        record_transition: bool,
    ) -> MoveCheckResult {
        let prev_captured = self.goat_captured;
        let prev_trapped = self.trapped_tiger;

        let mut prev_state = None;
        if record_transition {
            prev_state = Some(self.states_all_symmetry(None));
        }

        let move_eval: MoveCheckResult;
        if eval_res.is_none() {
            move_eval = self.check_move(source, target, None);
        } else {
            move_eval = eval_res.unwrap();
        }

        let r#type = if self.turn == -1 {
            MoveType::TigerMove
        } else if self.goat_counter < 20 {
            MoveType::GoatPlacement
        } else {
            MoveType::GoatMove
        };

        if !move_eval.is_valid {
            if self.game_over_on_invalid {
                self.move_reward_goat.push(0f32);
                self.move_reward_tiger.push(0f32);

                match self.turn {
                    -1 => {
                        self.transition_history.push(TransitionHistoryInstance {
                            r#move: (source, target),
                            state: prev_state.clone().unwrap(),
                            resulting_state: prev_state.unwrap(),
                            move_reward: self.gt_invalid_move.unwrap(),
                            is_terminal: true,
                            transition_type: r#type,
                        });

                        self.game_state = GameStatus::GoatWon;
                        *self.move_reward_goat.last_mut().unwrap() += self.g_win.unwrap();
                        *self.move_reward_tiger.last_mut().unwrap() +=
                            self.gt_invalid_move.unwrap();
                    }
                    1 => {
                        self.transition_history.push(TransitionHistoryInstance {
                            r#move: (source, target),
                            state: prev_state.clone().unwrap(),
                            resulting_state: prev_state.unwrap(),
                            move_reward: self.gt_invalid_move.unwrap(),
                            is_terminal: true,
                            transition_type: r#type,
                        });

                        self.game_state = GameStatus::TigerWon;
                        *self.move_reward_tiger.last_mut().unwrap() += self.t_win.unwrap();
                        *self.move_reward_goat.last_mut().unwrap() += self.gt_invalid_move.unwrap();
                    }
                    _ => {
                        panic!("Invalid turn value");
                    }
                }
            }

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
            self.pgn = crate::helpers::utils::coord_to_png_unit(source, target);
        } else {
            self.pgn.push('-');
            self.pgn
                .push_str(&crate::helpers::utils::coord_to_png_unit(source, target));
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
        let move_reward;
        if self.turn == -1 {
            *self.move_reward_goat.last_mut().unwrap() += self.g_move.unwrap();
            move_reward = self.move_reward_goat.last().unwrap().clone();
        } else {
            *self.move_reward_tiger.last_mut().unwrap() += self.t_move.unwrap();
            move_reward = self.move_reward_tiger.last().unwrap().clone();
        }

        if record_transition {
            let is_terminal = self.game_state != GameStatus::NotDecided;

            let resulting_state = self.states_all_symmetry(None);

            if let Some(last_transition) = self.transition_history.last_mut() {
                last_transition.move_reward -= move_reward;
            }

            self.transition_history.push(TransitionHistoryInstance {
                r#move: (source, target),
                state: prev_state.unwrap(),
                resulting_state,
                move_reward,
                is_terminal,
                transition_type: r#type,
            });
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

        // Source check and turn check
        match position[x as usize][y as usize] {
            0 => {
                return MoveCheckResult {
                    is_valid: false,
                    reason: "Source doesn't have a piece!".to_string(),
                    ..Default::default()
                }
            }
            1 if turn == 1 => (),
            -1 if turn == -1 => (),
            _ => {
                return MoveCheckResult {
                    is_valid: false,
                    reason: "Cannot move in other's turn!".to_string(),
                    ..Default::default()
                }
            }
        }
        // // Source has a piece check
        // if position[x as usize][y as usize] == 0 {
        //     return MoveCheckResult {
        //         is_valid: false,
        //         reason: "Source doesn't have a piece!".to_string(),
        //         ..Default::default()
        //     };
        // }
        //
        // // Turn check
        // if !((turn == 1 && position[x as usize][y as usize] == 1)
        //     || (turn == -1 && position[x as usize][y as usize] == -1))
        // {
        //     return MoveCheckResult {
        //         is_valid: false,
        //         reason: "Cannot move in other's turn!".to_string(),
        //         ..Default::default()
        //     };
        // }
        //
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
        if self.game_state != GameStatus::NotDecided {
            match self.game_state {
                GameStatus::TigerWon => {
                    return GameStatusCheckResult {
                        decided: true,
                        won_by: -1,
                    }
                }
                GameStatus::GoatWon => {
                    return GameStatusCheckResult {
                        decided: true,
                        won_by: 1,
                    }
                }
                _ => {
                    panic!("Invalid game state")
                }
            }
        } else if self.goat_captured >= 5 {
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
                                    new_move_state.make_move(Some([i, j]), [k, l], None, false);
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
                                    new_move_state.make_move(
                                        Some([i, j]),
                                        [i + k, j + l],
                                        None,
                                        false,
                                    );
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
                        new_move_state.make_move(None, [i, j], None, false);
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

    pub fn make_move_index(&mut self, index: usize) -> Option<&TransitionHistoryInstance> {
        let (source, destination);
        if self.turn == -1 {
            (source, destination) = BaghchalRS::i2m_tiger(index);
        } else if self.goat_counter >= 20 {
            (source, destination) = BaghchalRS::i2m_goat(index);
        } else {
            (source, destination) = BaghchalRS::i2m_placement(index);
        }
        self.make_move(source, destination, None, true);
        return self.transition_history.last();
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
}
