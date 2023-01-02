use lazy_static::lazy_static;
use regex::Regex;

#[derive(Debug)]
struct Instruction {
    count: usize,
    src: usize,
    dest: usize,
}

impl Instruction {
    fn parse(text: &str) -> Instruction {
        lazy_static! {
            static ref RE: Regex = Regex::new(r"^move (\d+) from (\d+) to (\d+)$").unwrap();
        }
        let caps = RE.captures(text).unwrap();
        Instruction {
            count: caps.get(1).unwrap().as_str().parse::<usize>().unwrap(),
            // Note the translation to make these 0-indexed
            src: caps.get(2).unwrap().as_str().parse::<usize>().unwrap() - 1,
            dest: caps.get(3).unwrap().as_str().parse::<usize>().unwrap() - 1,
        }
    }
}

#[derive(Debug)]
struct State {
    stacks: Vec<Vec<char>>,
}

impl State {
    fn from(text: &str) -> State {
        fn get_relevant_chars(line: &str) -> String {
            line[1..].chars().step_by(4).collect()
        }

        let mut stacks: Vec<Vec<char>> = vec![];

        // Iterate over lines backward so we can push naturally into the stacks
        let mut line_iter = text.lines().rev().map(|line| get_relevant_chars(line));

        // Initialize each stack using the "index line"
        for (idx, byte) in line_iter.next().unwrap().bytes().enumerate() {
            assert_eq!(idx as u8, byte - '0' as u8 - 1);
            stacks.push(vec![]);
        }

        // Push the initial data into all the stacks
        for data_line in line_iter {
            for (idx, char) in data_line.chars().enumerate() {
                if char != ' ' {
                    stacks.get_mut(idx).unwrap().push(char);
                }
            }
        }
        State { stacks }
    }

    fn apply_part1(&mut self, instruction: &Instruction) {
        for _ in 0..instruction.count {
            let char = self.stacks.get_mut(instruction.src).unwrap().pop().unwrap();
            self.stacks.get_mut(instruction.dest).unwrap().push(char);
        }
    }

    fn apply_part2(&mut self, instruction: &Instruction) {
        let mut chars: Vec<char> = vec![];

        let src_stack = self.stacks.get_mut(instruction.src).unwrap();
        for _ in 0..instruction.count {
            chars.push(src_stack.pop().unwrap())
        }

        let dest_stack = self.stacks.get_mut(instruction.dest).unwrap();
        for char in chars.iter().rev() {
            dest_stack.push(*char);
        }
    }

    fn get_stack_tops(&self) -> String {
        // Note the assumption that all stacks are non-empty, the problem seems to require this
        self.stacks
            .iter()
            .map(|stack| stack.last().unwrap())
            .collect()
    }
}

fn parse_input(input: &str) -> (State, Vec<Instruction>) {
    if let [state_input, instructions_input] = input.split("\n\n").collect::<Vec<_>>()[..] {
        (
            State::from(state_input),
            instructions_input
                .lines()
                .map(|line| Instruction::parse(line))
                .collect(),
        )
    } else {
        panic!("Could not parse input: {input}")
    }
}

fn part1(input: &str) -> String {
    let (mut state, instructions) = parse_input(input);
    for instruction in instructions {
        state.apply_part1(&instruction);
    }
    state.get_stack_tops()
}

fn part2(input: &str) -> String {
    let (mut state, instructions) = parse_input(input);
    for instruction in instructions {
        state.apply_part2(&instruction);
    }
    state.get_stack_tops()
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
