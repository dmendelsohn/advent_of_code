use std::collections::HashSet;

#[derive(Debug)]
struct Rucksack<'a> {
    contents: &'a str,
}

impl<'a> Rucksack<'a> {
    fn get_char_in_both_halves(&self) -> char {
        assert_eq!(self.contents.len() % 2, 0);
        let half_len = self.contents.len() / 2;
        let first: HashSet<char> = (&self.contents[..half_len]).chars().collect();
        let second: HashSet<char> = (&self.contents[half_len..]).chars().collect();
        let common_chars: Vec<&char> = first.intersection(&second).collect();
        assert_eq!(common_chars.len(), 1);
        **common_chars.first().unwrap()
    }
}

#[derive(Debug)]
struct Group<'a>(&'a Rucksack<'a>, &'a Rucksack<'a>, &'a Rucksack<'a>);

impl<'a> Group<'a> {
    fn get_common_char(&self) -> char {
        let first: HashSet<char> = self.0.contents.chars().collect();
        let second: HashSet<char> = self.1.contents.chars().collect();
        let third: HashSet<char> = self.2.contents.chars().collect();
        let mut common_chars: HashSet<char> = first;
        common_chars = common_chars.intersection(&second).copied().collect();
        common_chars = common_chars.intersection(&third).copied().collect();
        assert_eq!(common_chars.len(), 1);
        common_chars.iter().next().copied().unwrap()
    }
}

fn parse_input(input: &str) -> Vec<Rucksack> {
    input
        .lines()
        .map(|line| Rucksack { contents: line })
        .collect()
}

fn get_priority(c: char) -> usize {
    match c {
        'a'..='z' => c as usize - 'a' as usize + 1,
        'A'..='Z' => c as usize - 'A' as usize + 27,
        _ => panic!("Cannot determine priority value for {c}"),
    }
}

fn part1(input: &str) -> String {
    let rucksacks = parse_input(input);
    rucksacks
        .iter()
        .map(|r| get_priority(r.get_char_in_both_halves()))
        .sum::<usize>()
        .to_string()
}

fn part2(input: &str) -> String {
    let rucksacks = parse_input(input);
    let groups: Vec<Group> = rucksacks
        .chunks_exact(3)
        .map(|chunk| {
            let mut chunk_iter = chunk.iter();
            Group(
                chunk_iter.next().unwrap(),
                chunk_iter.next().unwrap(),
                chunk_iter.next().unwrap(),
            )
        })
        .collect();
    groups
        .iter()
        .map(|g| get_priority(g.get_common_char()))
        .sum::<usize>()
        .to_string()
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
