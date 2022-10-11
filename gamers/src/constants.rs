// For Tiger
pub static T_GOAT_CAPTURE: f32 = 2.0;
pub static T_GOT_TRAPPED: f32 = -1.0;
pub static T_TRAP_ESCAPE: f32 = 0.5;
pub static T_WIN: f32 = 5.0;
pub static T_LOSE: f32 = -5.0;
pub static T_DRAW: f32 = -3.0;

// For Goat
pub static G_GOAT_CAPTURED: f32 = -2.0;
pub static G_TIGER_TRAP: f32 = 1.0;
pub static G_TIGER_ESCAPE: f32 = -0.5;
pub static G_WIN: f32 = 5.0;
pub static G_LOSE: f32 = -5.0;
pub static G_DRAW: f32 = -3.0;

// Max Moves
pub static MAX_MOVES: i8 = 100;

pub static DEFAULT_GAME_LAYOUT: [[i8; 5]; 5] = [
    [-1, 0, 0, 0, -1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [-1, 0, 0, 0, -1],
];
