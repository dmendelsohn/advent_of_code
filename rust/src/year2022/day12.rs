use queues::*;
use std::fmt;
use std::fmt::Formatter;

struct Grid {
    values: Vec<Vec<char>>,
}

impl fmt::Debug for Grid {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        let grid_string = self
            .values
            .iter()
            .map(|row| row.into_iter().collect::<String>())
            .collect::<Vec<_>>()
            .join("\n");
        write!(f, "\n{}", grid_string)
    }
}

#[derive(Clone, Copy, Debug)]
struct Location {
    row: usize,
    col: usize,
}

impl Location {
    // Requires locations be manhattan distances 0 or 1 from each other
    fn direction_to(&self, other: Location) -> char {
        let row_offset = other.row as isize - self.row as isize;
        let col_offset = other.col as isize - self.col as isize;
        match (row_offset, col_offset) {
            (0, 0) => '.',
            (1, 0) => 'v',
            (-1, 0) => '^',
            (0, 1) => '>',
            (0, -1) => '<',
            _ => panic!("Cannot determine direction"),
        }
    }
}

impl Grid {
    // Return the grid, the start location, and the end location
    fn new(input: &str) -> (Self, Location, Location) {
        let mut start_location: Option<Location> = None;
        let mut end_location: Option<Location> = None;

        // Note locations of S and E, and replace them with a and z respectively
        let values: Vec<Vec<_>> = input
            .lines()
            .enumerate()
            .map(|(row, line)| {
                if let Some(col) = line.find('S') {
                    start_location = Some(Location { row, col });
                }
                if let Some(col) = line.find('E') {
                    end_location = Some(Location { row, col });
                }
                line.replace("S", "a").replace("E", "z").chars().collect()
            })
            .collect();

        let grid = Grid { values };
        (grid, start_location.unwrap(), end_location.unwrap())
    }

    fn is_valid_location(&self, row: isize, col: isize) -> bool {
        row >= 0
            && col >= 0
            && row < self.values.len() as isize
            && col < self.values[row as usize].len() as isize
    }

    fn get_reachable_neighbors(&self, location: Location) -> Vec<Location> {
        let mut result = vec![];
        let height = self.values[location.row][location.col] as usize;
        for (row_offset, col_offset) in [(0, 1), (0, -1), (1, 0), (-1, 0)] {
            let neighbor_row = location.row as isize + row_offset;
            let neighbor_col = location.col as isize + col_offset;
            if self.is_valid_location(neighbor_row, neighbor_col) {
                // Walking backward, cannot step down by more than 1
                let neighbor = Location {
                    row: neighbor_row as usize,
                    col: neighbor_col as usize,
                };
                let neighbor_height = self.values[neighbor.row][neighbor.col] as usize;
                if neighbor_height + 1 >= height {
                    result.push(neighbor);
                }
            }
        }
        result
    }

    fn get_a_locations(&self) -> Vec<Location> {
        let mut locations = vec![];
        for (row, row_data) in self.values.iter().enumerate() {
            for (col, char) in row_data.iter().enumerate() {
                if *char == 'a' {
                    locations.push(Location { row, col })
                }
            }
        }
        locations
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
struct SearchResult {
    // Represents most efficient direction toward end
    // One of '>', '<', 'v', '^', or '.' (for the end location itself)
    direction: char,
    // Number of steps required to reach end
    distance_to_end: usize,
}

#[allow(dead_code)]
fn pretty_print(search_results: &Vec<Vec<Option<SearchResult>>>) -> String {
    search_results
        .iter()
        .map(|row| {
            row.into_iter()
                .map({
                    |result| match result {
                        Some(result) => result.direction,
                        None => ' ',
                    }
                })
                .collect::<String>()
        })
        .collect::<Vec<_>>()
        .join("\n")
}

fn search(grid: &Grid, end: Location) -> Vec<Vec<Option<SearchResult>>> {
    let num_rows = grid.values.len();
    let num_cols = grid.values[0].len();
    let mut results = vec![vec![None; num_cols]; num_rows];

    // Seed the results and BFS queue with our starting point
    // We search in reverse starting from the end
    results[end.row][end.col] = Some(SearchResult {
        direction: '.',
        distance_to_end: 0,
    });
    let mut queue = queue![end];

    while let Ok(location) = queue.remove() {
        // Visit neighbors that are reachable and have not yet been visited
        let neighbors_to_visit: Vec<_> = grid
            .get_reachable_neighbors(location)
            .into_iter()
            .filter(|n| results[n.row][n.col] == None)
            .collect();

        // For each such neighbor, compute search result and push to queue
        let distance_to_end = results[location.row][location.col].unwrap().distance_to_end;
        for neighbor in neighbors_to_visit {
            results[neighbor.row][neighbor.col] = Some(SearchResult {
                direction: neighbor.direction_to(location),
                distance_to_end: distance_to_end + 1,
            });
            queue.add(neighbor).expect("Could not add to queue");
        }
    }

    results
}

fn part1(input: &str) -> String {
    let (grid, start, end) = Grid::new(input);
    let search_results = search(&grid, end);

    search_results[start.row][start.col]
        .unwrap()
        .distance_to_end
        .to_string()
}

fn part2(input: &str) -> String {
    let (grid, _, end) = Grid::new(input);
    let search_results = search(&grid, end);

    grid.get_a_locations()
        .iter()
        .filter_map(|loc| match search_results[loc.row][loc.col] {
            Some(search_result) => Some(search_result.distance_to_end),
            None => None,
        })
        .min()
        .unwrap()
        .to_string()
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
