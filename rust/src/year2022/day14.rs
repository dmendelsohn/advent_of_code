use std::cmp::Ordering;

#[derive(Clone, Copy, Debug, PartialEq)]
struct Location {
    row: usize,
    col: usize,
}

impl Location {
    // Get the row + col offset of a single step toward the other location
    fn step_toward(&self, other: &Location) -> (isize, isize) {
        if self.row == other.row {
            match self.col.cmp(&other.col) {
                Ordering::Less => (0, 1),
                Ordering::Greater => (0, -1),
                Ordering::Equal => panic!("Cannot step toward self"),
            }
        } else if self.col == other.col {
            match self.row.cmp(&other.row) {
                Ordering::Less => (1, 0),
                Ordering::Greater => (-1, 0),
                Ordering::Equal => panic!("Cannot step toward self"),
            }
        } else {
            panic!("Cannot step diagonally");
        }
    }

    fn apply_offset(&self, row_offset: isize, col_offset: isize) -> Location {
        let row = self.row as isize + row_offset;
        let col = self.col as isize + col_offset;
        assert!(row >= 0);
        assert!(col >= 0);
        Location {
            row: row as usize,
            col: col as usize,
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
enum Object {
    Rock,
    Sand,
}

struct Cave {
    spaces: Vec<Vec<Option<Object>>>,
    source_location: Location,
}

impl Cave {
    fn new(rock_lines: Vec<RockLine>, source_location: Location) -> Self {
        // Initialize empty spaces with the minimum bounding box
        let max_row = rock_lines
            .iter()
            .map(|line| line.vertices.iter().map(|vertex| vertex.row).max().unwrap())
            .max()
            .unwrap();
        let max_col = rock_lines
            .iter()
            .map(|line| line.vertices.iter().map(|vertex| vertex.col).max().unwrap())
            .max()
            .unwrap();
        let mut spaces = vec![vec![None; max_col + 1]; max_row + 1];

        // Fill in the rocks
        for rock_line in rock_lines {
            for rock_location in rock_line.to_locations() {
                spaces[rock_location.row][rock_location.col] = Some(Object::Rock);
            }
        }

        Cave {
            spaces,
            source_location,
        }
    }

    fn get(&self, location: Location) -> Option<Object> {
        if location.row < self.spaces.len() && location.col < self.spaces[location.row].len() {
            self.spaces[location.row][location.col]
        } else {
            None
        }
    }

    fn place_sand(&mut self) -> Option<Location> {
        if self.get(self.source_location) != None {
            return None; // Can't even get an initial position for sand
        }

        let mut sand_location = self.source_location.clone();
        loop {
            // If we're already at max row, return None
            if sand_location.row == self.spaces.len() - 1 {
                return None;
            }

            // Compute downward neighbors in priority order
            let neighbors = [
                Location {
                    row: sand_location.row + 1,
                    col: sand_location.col,
                },
                Location {
                    row: sand_location.row + 1,
                    col: sand_location.col - 1,
                },
                Location {
                    row: sand_location.row + 1,
                    col: sand_location.col + 1,
                },
            ];

            match neighbors
                .iter()
                .find(|neighbor| self.get(**neighbor) == None)
            {
                // Move sand to first empty neighbor
                Some(neighbor) => sand_location = neighbor.clone(),
                // Or finalize sand position and return it
                None => {
                    self.spaces[sand_location.row][sand_location.col] = Some(Object::Sand);
                    return Some(sand_location);
                }
            }
        }
    }

    #[allow(dead_code)]
    fn pretty_print(&self, min_col: usize, max_col: usize) -> String {
        let mut pretty_str = String::new();
        for row_data in &self.spaces {
            pretty_str.push('\n');
            for space in &row_data[min_col..=max_col] {
                pretty_str.push(match space {
                    Some(Object::Rock) => '#',
                    Some(Object::Sand) => 'o',
                    None => '.',
                })
            }
        }
        pretty_str
    }
}

#[derive(Debug)]
struct RockLine {
    vertices: Vec<Location>,
}

impl RockLine {
    fn parse(text: &str) -> Self {
        let vertices = text
            .split(" -> ")
            .map(|vertex| {
                if let [col, row] = vertex.split(",").collect::<Vec<_>>()[..] {
                    Location {
                        row: row.parse::<usize>().unwrap(),
                        col: col.parse::<usize>().unwrap(),
                    }
                } else {
                    panic!("Could not parse vertex {} from rock line {}", vertex, text);
                }
            })
            .collect();
        RockLine { vertices }
    }

    fn to_locations(&self) -> Vec<Location> {
        let mut vertices = self.vertices.iter();
        let mut current_location = vertices.next().unwrap().clone();
        let mut locations = vec![current_location.clone()];
        while let Some(next_vertex) = vertices.next() {
            let (row_offset, col_offset) = current_location.step_toward(&next_vertex);
            while current_location != *next_vertex {
                current_location = current_location.apply_offset(row_offset, col_offset);
                locations.push(current_location.clone());
            }
        }
        locations
    }
}

fn parse_input(input: &str) -> Vec<RockLine> {
    input.lines().map(|line| RockLine::parse(line)).collect()
}

fn part1(input: &str) -> String {
    let mut cave = Cave::new(parse_input(input), Location { row: 0, col: 500 });

    let mut num_sand_at_rest = 0;
    while let Some(_) = cave.place_sand() {
        num_sand_at_rest += 1
    }

    num_sand_at_rest.to_string()
}

fn part2(input: &str) -> String {
    let mut rock_lines = parse_input(input);
    let max_row = rock_lines
        .iter()
        .map(|line| line.vertices.iter().map(|vertex| vertex.row).max().unwrap())
        .max()
        .unwrap();

    rock_lines.push({
        RockLine {
            vertices: vec![
                Location {
                    row: max_row + 2,
                    col: 0,
                },
                Location {
                    row: max_row + 2,
                    col: 1000,
                },
            ],
        }
    });
    let mut cave = Cave::new(rock_lines, Location { row: 0, col: 500 });

    let mut num_sand_at_rest = 0;
    while let Some(_) = cave.place_sand() {
        num_sand_at_rest += 1
    }

    num_sand_at_rest.to_string()
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
