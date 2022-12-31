enum RoundOutcome {
    Win,
    Loss,
    Draw,
}

impl RoundOutcome {
    fn get_points(&self) -> usize {
        match *self {
            RoundOutcome::Win => 6,
            RoundOutcome::Draw => 3,
            RoundOutcome::Loss => 0,
        }
    }
}

enum Shape {
    Rock,
    Paper,
    Scissors,
}

impl Shape {
    /// Using this helper value, we say you beat opponent if you're shape
    /// has a value that is one higher than your opponent's (modulo 3)
    fn get_value(&self) -> usize {
        match *self {
            Shape::Rock => 1,
            Shape::Paper => 2,
            Shape::Scissors => 3,
        }
    }

    fn get_round_outcome(&self, other: &Self) -> RoundOutcome {
        match (3 + self.get_value() - other.get_value()) % 3 {
            0 => RoundOutcome::Draw,
            1 => RoundOutcome::Win,
            2 => RoundOutcome::Loss,
            _x => panic!("Unexpected different in shape values {_x}"),
        }
    }

    fn from_desired_outcome(outcome: &RoundOutcome, other: &Self) -> Self {
        let shape_value = other.get_value()
            + match outcome {
                RoundOutcome::Draw => 0,
                RoundOutcome::Win => 1,
                RoundOutcome::Loss => 2,
            };
        match shape_value % 3 {
            1 => Shape::Rock,
            2 => Shape::Paper,
            0 => Shape::Scissors,
            _x => panic!("Unexpected shape value {_x}"),
        }
    }
}

struct Round {
    opponent_shape: Shape,
    you_shape: Shape,
}

impl Round {
    fn from(text: &str) -> Round {
        assert_eq!(text.len(), 3);
        let opponent_shape = match text.chars().nth(0).unwrap() {
            'A' => Shape::Rock,
            'B' => Shape::Paper,
            'C' => Shape::Scissors,
            _ => panic!("Could not parse round: {text}"),
        };
        let you_shape = match text.chars().nth(2).unwrap() {
            'X' => Shape::Rock,
            'Y' => Shape::Paper,
            'Z' => Shape::Scissors,
            _ => panic!("Could not parse round: {text}"),
        };
        Round {
            opponent_shape,
            you_shape,
        }
    }

    fn from_part2(text: &str) -> Round {
        assert_eq!(text.len(), 3);
        let opponent_shape = match text.chars().nth(0).unwrap() {
            'A' => Shape::Rock,
            'B' => Shape::Paper,
            'C' => Shape::Scissors,
            _ => panic!("Could not parse round: {text}"),
        };
        let desired_outcome = match text.chars().nth(2).unwrap() {
            'X' => RoundOutcome::Loss,
            'Y' => RoundOutcome::Draw,
            'Z' => RoundOutcome::Win,
            _ => panic!("Could not parse round: {text}"),
        };
        let you_shape = Shape::from_desired_outcome(&desired_outcome, &opponent_shape);
        Round {
            opponent_shape,
            you_shape,
        }
    }

    fn get_score(&self) -> usize {
        let round_outcome = self.you_shape.get_round_outcome(&self.opponent_shape);
        round_outcome.get_points() + self.you_shape.get_value()
    }
}

fn part1(input: &str) -> String {
    input
        .lines()
        .map(|line| Round::from(line.trim()).get_score())
        .sum::<usize>()
        .to_string()
}

fn part2(input: &str) -> String {
    input
        .lines()
        .map(|line| Round::from_part2(line.trim()).get_score())
        .sum::<usize>()
        .to_string()
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
