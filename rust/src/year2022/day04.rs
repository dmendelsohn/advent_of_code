#[derive(Clone, Copy, Debug)]
struct Assignment {
    low: usize,
    high: usize,
}

impl Assignment {
    fn from(text: &str) -> Assignment {
        let nums: Vec<usize> = text
            .split("-")
            .map(|x| x.parse::<usize>().unwrap())
            .collect();
        if let [low, high] = nums[..] {
            return Assignment { low, high };
        }
        panic!("Could not parse assignment from text: {text}");
    }

    fn contains(&self, other: &Assignment) -> bool {
        self.low <= other.low && self.high >= other.high
    }

    fn overlaps(&self, other: &Assignment) -> bool {
        self.low <= other.high && self.high >= other.low
    }
}

fn parse_input(input: &str) -> Vec<(Assignment, Assignment)> {
    input
        .lines()
        .map(|line| {
            let assignments: Vec<Assignment> =
                line.split(",").map(|a| Assignment::from(a)).collect();
            if let [first, second] = assignments[..] {
                (first, second)
            } else {
                panic!("Could not parse line {line}");
            }
        })
        .collect()
}

fn has_contained_pair(assignment_pair: (Assignment, Assignment)) -> bool {
    return assignment_pair.0.contains(&assignment_pair.1)
        || assignment_pair.1.contains(&assignment_pair.0);
}

fn has_overlapping_pair(assignment_pair: (Assignment, Assignment)) -> bool {
    assignment_pair.0.overlaps(&assignment_pair.1)
}

fn part1(input: &str) -> String {
    let assignment_pairs = parse_input(input);
    assignment_pairs
        .into_iter()
        .filter(|pair| has_contained_pair(*pair))
        .count()
        .to_string()
}

fn part2(input: &str) -> String {
    let assignment_pairs = parse_input(input);
    assignment_pairs
        .into_iter()
        .filter(|pair| has_overlapping_pair(*pair))
        .count()
        .to_string()
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
