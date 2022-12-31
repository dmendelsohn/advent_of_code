#[derive(Debug)]
struct Inventory {
    items: Vec<i32>,
}

impl Inventory {
    fn from(text: &str) -> Inventory {
        Inventory {
            items: text
                .split("\n")
                .map(|x| x.parse::<i32>().unwrap())
                .collect(),
        }
    }

    fn total(&self) -> i32 {
        self.items.iter().sum()
    }
}

fn parse_input(text: &str) -> Vec<Inventory> {
    text.trim()
        .split("\n\n")
        .map(|x| Inventory::from(x))
        .collect()
}

fn part1(input: &str) -> String {
    let inventories = parse_input(input);
    let largest_inventory = inventories.iter().max_by_key(|i| i.total()).unwrap();
    largest_inventory.total().to_string()
}

fn part2(input: &str) -> String {
    let mut inventories = parse_input(input);
    inventories.sort_by_key(|i| i.total());
    inventories.reverse();
    (&inventories[0..=2])
        .iter()
        .map(|i| i.total())
        .sum::<i32>()
        .to_string()
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
