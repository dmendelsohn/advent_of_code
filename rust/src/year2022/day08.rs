use std::collections::{HashMap, HashSet};

#[derive(Copy, Clone, Debug, Eq, Hash, PartialEq)]
struct Location {
    row: isize,
    col: isize,
}

#[derive(Debug)]
struct Offset {
    row_offset: isize,
    col_offset: isize,
}

#[derive(Debug)]
struct Forest {
    num_rows: usize,
    num_cols: usize,
    heights: HashMap<Location, usize>,
}

impl Forest {
    fn get_num_visible_locations(&self) -> usize {
        let mut visible_locations: HashSet<Location> = HashSet::new();
        for col in 0..self.num_cols {
            // Look down from top
            self.find_visible_locations(
                &Location {
                    row: 0,
                    col: col as isize,
                },
                &Offset {
                    row_offset: 1,
                    col_offset: 0,
                },
                &mut visible_locations,
            );
            // Look up from bottom
            self.find_visible_locations(
                &Location {
                    row: self.num_rows as isize - 1,
                    col: col as isize,
                },
                &Offset {
                    row_offset: -1,
                    col_offset: 0,
                },
                &mut visible_locations,
            )
        }
        for row in 0..self.num_rows {
            // Look rightward from left side
            self.find_visible_locations(
                &Location {
                    row: row as isize,
                    col: 0,
                },
                &Offset {
                    row_offset: 0,
                    col_offset: 1,
                },
                &mut visible_locations,
            );
            // Look leftward from the right
            self.find_visible_locations(
                &Location {
                    row: row as isize,
                    col: self.num_cols as isize - 1,
                },
                &Offset {
                    row_offset: 0,
                    col_offset: -1,
                },
                &mut visible_locations,
            )
        }
        visible_locations.len()
    }

    fn find_visible_locations(
        &self,
        start_location: &Location,
        offset: &Offset,
        result: &mut HashSet<Location>,
    ) {
        result.insert(start_location.clone());
        let mut current_location = start_location.clone();
        let mut largest_height_so_far = self.heights.get(&start_location).unwrap();
        loop {
            current_location.row += offset.row_offset;
            current_location.col += offset.col_offset;
            match self.heights.get(&current_location) {
                Some(height) => {
                    if height > largest_height_so_far {
                        largest_height_so_far = height;
                        result.insert(current_location);
                    }
                }
                None => break,
            }
        }
    }

    fn get_scenic_score(&self, location: &Location) -> usize {
        let down = self.get_num_trees_from_interior(
            location,
            &Offset {
                row_offset: 1,
                col_offset: 0,
            },
        );
        let up = self.get_num_trees_from_interior(
            location,
            &Offset {
                row_offset: -1,
                col_offset: 0,
            },
        );
        let right = self.get_num_trees_from_interior(
            location,
            &Offset {
                row_offset: 0,
                col_offset: 1,
            },
        );
        let left = self.get_num_trees_from_interior(
            location,
            &Offset {
                row_offset: 0,
                col_offset: -1,
            },
        );
        up * down * left * right
    }

    fn get_num_trees_from_interior(&self, origin: &Location, offset: &Offset) -> usize {
        let mut num: usize = 0;
        let origin_height = self.heights.get(&origin).unwrap();
        let mut current_location = origin.clone();
        loop {
            current_location.row += offset.row_offset;
            current_location.col += offset.col_offset;

            match self.heights.get(&current_location) {
                Some(height) if height < origin_height => {
                    num += 1;
                }
                Some(_) => {
                    // This one counts, but we stop iterating
                    num += 1;
                    break;
                }
                None => break,
            }
        }
        num
    }
}

fn parse_input(input: &str) -> Forest {
    let mut forest = Forest {
        num_rows: input.lines().count(),
        num_cols: input.lines().next().unwrap().len(),
        heights: HashMap::new(),
    };
    for (row, line) in input.lines().enumerate() {
        for (col, char) in line.chars().enumerate() {
            let height = char.to_digit(10).unwrap() as usize;
            forest.heights.insert(
                Location {
                    row: row as isize,
                    col: col as isize,
                },
                height,
            );
        }
    }
    forest
}

fn part1(input: &str) -> String {
    let forest = parse_input(input);
    forest.get_num_visible_locations().to_string()
}

fn part2(input: &str) -> String {
    let forest = parse_input(input);
    forest
        .heights
        .keys()
        .map(|loc| forest.get_scenic_score(loc))
        .max()
        .unwrap()
        .to_string()
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
