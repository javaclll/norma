use crate::constants;
use crate::Baghchal;
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

#[pyclass]
#[derive(Debug, PartialEq, Clone, Copy, Serialize, Deserialize)]
pub enum GameStatus {
    NotDecided,
    GoatWon,
    TigerWon,
    Draw,
}

#[pymethods]
impl GameStatus {
    fn to_value(&self) -> i8 {
        match self {
            Self::NotDecided => 0,
            Self::GoatWon => 1,
            Self::TigerWon => 2,
            Self::Draw => 3,
        }
    }

    #[staticmethod]
    fn from_value(value: i8) -> GameStatus {
        match value {
            0 => GameStatus::NotDecided,
            1 => GameStatus::GoatWon,
            2 => GameStatus::TigerWon,
            3 => GameStatus::Draw,
            _ => GameStatus::NotDecided,
        }
    }
}

pub type Move = (Option<[i8; 2]>, [i8; 2]);

#[pyclass]
#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub struct GameStateInstance {
    #[pyo3(get)]
    pub board: [[i8; 5]; 5],

    #[pyo3(get)]
    pub goat_count: i8,

    #[pyo3(get)]
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

#[pymethods]
impl GameStateInstance {
    fn to_str(&self) -> String
    where
        Self: Serialize,
    {
        return serde_json::to_string(&self).unwrap();
    }
}

#[pyclass]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MoveCheckResult {
    #[pyo3(get)]
    pub is_valid: bool,
    #[pyo3(get)]
    pub is_place_move: bool,
    #[pyo3(get)]
    pub is_capture_move: bool,
    #[pyo3(get)]
    pub capture_piece: Option<[i8; 2]>,
    #[pyo3(get)]
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

#[pymethods]
impl MoveCheckResult {
    fn to_str(&self) -> String
    where
        Self: Serialize,
    {
        return serde_json::to_string(&self).unwrap();
    }
}

#[pyclass]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameStatusCheckResult {
    #[pyo3(get)]
    pub decided: bool,

    #[pyo3(get)]
    pub won_by: i8,
}

#[pymethods]
impl GameStatusCheckResult {
    fn to_str(&self) -> String
    where
        Self: Serialize,
    {
        return serde_json::to_string(&self).unwrap();
    }
}

#[pyclass]
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PossibleMove {
    #[pyo3(get)]
    pub r#move: Move,

    #[pyo3(get)]
    pub resulting_state: Baghchal,
}

#[pymethods]
impl PossibleMove {
    fn to_str(&self) -> String
    where
        Self: Serialize,
    {
        return serde_json::to_string(&self).unwrap();
    }
}
