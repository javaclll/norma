use super::types::Move;

pub fn two_step_merge(input: Vec<f32>) -> Vec<f32> {
    let mut output = Vec::new();

    for i in (0..input.len()).step_by(2) {
        if i + 1 < input.len() {
            let sum = input[i] + input[i + 1];
            output.push(sum);
        }
    }

    return output;
}

pub fn merge_rewards(goat_rewards: &Vec<f32>, tiger_rewards: &Vec<f32>) -> Vec<f32> {
    let mut rewards_g = goat_rewards.clone();
    let mut rewards_t = tiger_rewards.clone();

    rewards_t.remove(0);

    if rewards_g.len() % 2 != 0 {
        rewards_g.push(0.0)
    }

    if rewards_t.len() % 2 != 0 {
        rewards_t.push(0.0)
    }

    rewards_g = two_step_merge(rewards_g);
    rewards_t = two_step_merge(rewards_t);

    let mut rewards: Vec<f32> = Vec::new();

    for i in 0..rewards_g.len().max(rewards_t.len()) {
        let ith_re_g = rewards_g.get(i);
        let ith_re_t = rewards_t.get(i);

        if let Some(reward) = ith_re_g {
            rewards.push(*reward);
        }

        if let Some(reward) = ith_re_t {
            rewards.push(*reward);
        }
    }

    return rewards;
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

pub fn rotate_matrix(matrix: [[i8; 5]; 5], times: i8) -> [[i8; 5]; 5] {
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

pub fn y_reflect_matrix(matrix: [[i8; 5]; 5]) -> [[i8; 5]; 5] {
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

pub fn x_reflect_matrix(matrix: [[i8; 5]; 5]) -> [[i8; 5]; 5] {
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

pub fn origin_reflect_matrix(matrix: [[i8; 5]; 5]) -> [[i8; 5]; 5] {
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

pub fn get_transformed_boards(
    matrix: [[i8; 5]; 5],
    source_map: [[i8; 5]; 5],
    destination_map: [[i8; 5]; 5],
) -> [([[i8; 5]; 5], [[i8; 5]; 5], [[i8; 5]; 5]); 7] {
    return [
        (matrix, source_map, destination_map),
        (
            rotate_matrix(matrix, 1),
            rotate_matrix(source_map, 1),
            rotate_matrix(destination_map, 1),
        ),
        (
            rotate_matrix(matrix, 2),
            rotate_matrix(source_map, 2),
            rotate_matrix(destination_map, 2),
        ),
        (
            rotate_matrix(matrix, 3),
            rotate_matrix(source_map, 3),
            rotate_matrix(destination_map, 3),
        ),
        (
            x_reflect_matrix(matrix),
            x_reflect_matrix(source_map),
            x_reflect_matrix(destination_map),
        ),
        (
            y_reflect_matrix(matrix),
            y_reflect_matrix(source_map),
            y_reflect_matrix(destination_map),
        ),
        (
            origin_reflect_matrix(matrix),
            origin_reflect_matrix(source_map),
            origin_reflect_matrix(destination_map),
        ),
    ];
}

pub fn action_to_vector(source: Option<[i8; 2]>, destination: [i8; 2]) -> Vec<i8> {
    let mut vector = Vec::<i8>::with_capacity(20);

    if source.is_none() {
        vector.append(&mut [0, 0, 0, 0, 0, 0, 0, 0, 0, 0].to_vec());
    } else {
        vector.append(&mut pos_dec(source.unwrap()[0]));
        vector.append(&mut pos_dec(source.unwrap()[1]));
    }

    vector.append(&mut pos_dec(destination[0]));
    vector.append(&mut pos_dec(destination[1]));

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

pub fn undo_symmetry(
    source_map: [[i8; 5]; 5],
    dest_map: [[i8; 5]; 5],
    symmetry: i8,
) -> ([[i8; 5]; 5], [[i8; 5]; 5]) {
    match symmetry {
        0 => return (source_map, dest_map),
        1 => return (rotate_matrix(source_map, 3), rotate_matrix(dest_map, 3)),
        2 => return (rotate_matrix(source_map, 2), rotate_matrix(dest_map, 2)),
        3 => return (rotate_matrix(source_map, 1), rotate_matrix(dest_map, 1)),
        4 => return (x_reflect_matrix(source_map), x_reflect_matrix(dest_map)),
        5 => return (y_reflect_matrix(source_map), y_reflect_matrix(dest_map)),
        6 => {
            return (
                origin_reflect_matrix(source_map),
                origin_reflect_matrix(dest_map),
            )
        }
        _ => panic!("Invalid symmetry!"),
    };
}

pub fn pgn_unit_to_coord(pgn: String) -> Move {
    let source: Option<[i8; 2]>;

    let pgn_iter = pgn.chars().collect::<Vec<char>>();

    if *pgn_iter.get(1).unwrap() == 'X' {
        source = None;
    } else {
        source = Some([
            5 - pgn_iter.get(1).unwrap().to_digit(10).unwrap() as i8,
            char_to_cord(*pgn_iter.get(0).unwrap()),
        ]);
    }

    let destination = [
        5 - pgn_iter.get(3).unwrap().to_digit(10).unwrap() as i8,
        char_to_cord(*pgn_iter.get(2).unwrap()),
    ];

    return (source, destination);
}

pub fn coord_to_png_unit(source: Option<[i8; 2]>, destination: [i8; 2]) -> String {
    let mut unit = String::new();

    // Source coordinates to PGN
    if source.is_none() {
        unit = "XX".to_string();
    } else {
        unit.push(cord_to_char(source.unwrap()[1]));
        unit.push_str(&(5 - source.unwrap()[0]).to_string());
    };

    // Destination coordinates to PGN
    unit.push(cord_to_char(destination[1]));
    unit.push_str(&(5 - destination[0]).to_string());

    return unit;
}
