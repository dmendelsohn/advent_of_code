#[derive(Debug)]
enum Instruction {
    Addx(isize),
    Noop,
}

#[derive(Debug)]
struct Signal {
    // value at index i represents value during cycle i
    values: Vec<isize>,
}

impl Signal {
    fn new() -> Self {
        // There is no 0th cycle, and the 1st cycle has value 1
        Signal { values: vec![1, 1] }
    }

    fn handle(&mut self, instruction: &Instruction) {
        // Either way, the next cycle will have the same value as the current one
        self.values.push(*self.values.last().unwrap());
        // Then, in the case of an addx, the subsequent cycle will be changed
        if let Instruction::Addx(addx_value) = instruction {
            self.values.push(*self.values.last().unwrap() + addx_value);
        }
    }

    fn get_line(&self, start_index: usize, line_width: usize) -> String {
        let mut line = String::new();
        for cursor_position in 0..line_width {
            let sprite_position = self.values[start_index + cursor_position] as isize;
            let char = if (sprite_position - (cursor_position as isize)).abs() <= 1 {
                '#'
            } else {
                '.'
            };
            line.push(char);
        }
        String::from(line)
    }
}

fn parse_input(input: &str) -> Vec<Instruction> {
    input
        .lines()
        .map(|line| match line.split(" ").collect::<Vec<_>>()[..] {
            ["addx", value] => Instruction::Addx(value.parse::<isize>().unwrap()),
            ["noop"] => Instruction::Noop,
            _ => panic!("Could not parse line {line}"),
        })
        .collect()
}

fn part1(input: &str) -> String {
    let instructions = parse_input(input);

    // Build the signal
    let mut signal = Signal::new();
    for inst in instructions {
        signal.handle(&inst);
    }

    // Calculate total signal strength
    let mut total_signal_strength = 0;
    for cycle in [20, 60, 100, 140, 180, 220] {
        total_signal_strength += signal.values[cycle] * cycle as isize;
    }

    total_signal_strength.to_string()
}

fn part2(input: &str) -> String {
    let instructions = parse_input(input);

    // Build the signal
    let mut signal = Signal::new();
    for inst in instructions {
        signal.handle(&inst);
    }

    // Calculate the number of lines (checking that the last line is full-width)
    assert_eq!(signal.values.len() % 40, 2); // 0th index and last index don't count
    let num_lines = signal.values.len() / 40;

    // Build the output line by line
    let mut output: Vec<String> = vec![String::from("\n")];
    for line_idx in 0..num_lines {
        let mut line = signal.get_line(line_idx * 40 + 1, 40);
        output.push(line);
    }

    output.join("\n")
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    // Note: here the answer has to be visually interpreted as EHPZPJGL
    println!("Solution to part 2: {}", part2(input));
}
