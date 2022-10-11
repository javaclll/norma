use crate::constants;
use crate::bagchal::Bagchal;

#[derive(Debug, PartialEq, Clone)]
pub enum GameState {
    NotDecided,
    GoatWon,
    TigerWon,
    Draw,
}

pub type Move = (Option<[i8; 2]>, [i8; 2]);

#[derive(Debug, Clone)]
pub struct GameStateInstance {
    pub board: [[i8; 5]; 5],
    pub goat_count: i8,
    pub goat_captured: i8,
}

impl Default for GameStateInstance {
    fn default() -> Self {
        Self {
            board: constants::DEFAULT_GAME_LAYOUT,
            goat_count: 0,
            goat_captured: 0,
        }
    }
}

#[derive(Debug, Clone)]
pub struct MoveCheckResult {
    pub is_valid: bool,
    pub is_place_move: bool,
    pub is_capture_move: bool,
    pub capture_piece: Option<[i8; 2]>,
    pub reason: String,
}

impl Default for MoveCheckResult {
    fn default() -> Self {
        Self {
            is_valid: true,
            is_capture_move: false,
            capture_piece: None,
            is_place_move: false,
            reason: "Default move!".to_string(),
        }
    }
}

#[derive(Debug, Clone)]
pub struct GameStatusCheckResult {
    pub decided: bool,
    pub won_by: i8,
}

#[derive(Debug, Clone)]
pub struct PossibleMove {
    pub r#move: Move,
    pub resulting_state: Bagchal,
}
