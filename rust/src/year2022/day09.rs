use std::collections::HashSet;

#[derive(Debug)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

#[derive(Debug)]
struct Instruction {
    direction: Direction,
    count: usize,
}

impl Instruction {
    fn from(text: &str) -> Self {
        let parts: Vec<&str> = text.split(" ").collect();
        if let [direction, count] = parts[..] {
            let count = count.parse::<usize>().unwrap();
            let direction = match direction {
                "U" => Direction::Up,
                "D" => Direction::Down,
                "L" => Direction::Left,
                "R" => Direction::Right,
                _ => panic!("Could not parse direction: {direction}"),
            };
            Instruction { direction, count }
        } else {
            panic!("Could not parse instruction: {text}");
        }
    }
}

#[derive(Copy, Clone, Debug, Eq, Hash, PartialEq)]
struct Location {
    row: isize,
    col: isize,
}

impl Location {
    fn is_adjacent(&self, other: &Location) -> bool {
        (self.row - other.row).abs() <= 1 && (self.col - other.col).abs() <= 1
    }

    fn snap_to(&mut self, other: &Location) {
        if !self.is_adjacent(other) {
            // Move to other locations, plus half the difference.
            // That way distances of 2 become 1, and distances of 1 become 0.
            self.row = other.row + (self.row - other.row) / 2;
            self.col = other.col + (self.col - other.col) / 2;
        }
    }
}

#[derive(Debug)]
struct State {
    knots: Vec<Location>,
}

impl State {
    fn new(num_knots: usize) -> State {
        assert!(num_knots > 0);
        State {
            knots: vec![Location { row: 0, col: 0 }; num_knots],
        }
    }

    fn tail(&self) -> &Location {
        self.knots.last().unwrap()
    }

    fn update(&mut self, direction: &Direction) {
        // Move the head in the specified direction
        let mut head = self.knots[0];
        match direction {
            Direction::Up => {
                head.row -= 1;
            }
            Direction::Down => {
                head.row += 1;
            }
            Direction::Left => {
                head.col -= 1;
            }
            Direction::Right => {
                head.col += 1;
            }
        }
        self.knots[0] = head;

        // Then reconcile the other knots
        for i in 1..self.knots.len() {
            let predecessor = self.knots[i - 1];
            self.knots[i].snap_to(&predecessor)
        }
    }
}

fn parse_input(input: &str) -> Vec<Instruction> {
    input.lines().map(|line| Instruction::from(line)).collect()
}

fn count_tail_locations(instructions: Vec<Instruction>, num_knots: usize) -> usize {
    let mut state = State::new(num_knots);
    let mut tail_positions = HashSet::new();
    tail_positions.insert(state.tail().clone());
    for instruction in instructions {
        for _ in 0..instruction.count {
            state.update(&instruction.direction);
            tail_positions.insert(state.tail().clone());
        }
    }
    tail_positions.len()
}

fn part1(input: &str) -> String {
    count_tail_locations(parse_input(input), 2).to_string()
}

fn part2(input: &str) -> String {
    count_tail_locations(parse_input(input), 10).to_string()
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
