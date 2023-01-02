use std::collections::HashSet;

fn find_marker(input: &str, window_size: usize) -> usize {
    let chars: Vec<char> = input.chars().collect();
    for (start_idx, window) in chars.windows(window_size).enumerate() {
        if window.iter().collect::<HashSet<&char>>().len() == window_size {
            return start_idx + window_size;
        }
    }
    panic!("Could not find solution")
}

fn part1(input: &str) -> String {
    find_marker(input, 4).to_string()
}

fn part2(input: &str) -> String {
    find_marker(input, 14).to_string()
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
