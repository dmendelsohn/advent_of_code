use std::cmp::Reverse;
use std::fmt;

type MonkeyId = usize;

#[derive(Clone, Copy, Debug)]
struct Item {
    id: usize,
    value: isize,
}

struct Operation<'a>(Box<dyn Fn(isize) -> isize + 'a>);

impl fmt::Debug for Operation<'_> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "<operation>")
    }
}

#[derive(Debug)]
struct Monkey<'a> {
    id: MonkeyId,
    starting_items: Vec<Item>,
    operation: Operation<'a>,
    test_modulo: isize,
    true_dest: MonkeyId,
    false_dest: MonkeyId,
}

impl<'a> Monkey<'a> {
    fn parse(text: &'a str) -> Self {
        let mut lines = text.lines();
        let id = Monkey::parse_id(lines.next().unwrap());
        Monkey {
            id,
            starting_items: Monkey::parse_starting_items(lines.next().unwrap(), id),
            operation: Monkey::parse_operation(lines.next().unwrap()),
            test_modulo: Monkey::parse_test_modulo(lines.next().unwrap()),
            true_dest: Monkey::parse_true_dest(lines.next().unwrap()),
            false_dest: Monkey::parse_false_dest(lines.next().unwrap()),
        }
    }

    fn parse_id(line: &str) -> MonkeyId {
        line.strip_prefix("Monkey ")
            .unwrap()
            .strip_suffix(":")
            .unwrap()
            .parse()
            .unwrap()
    }

    fn parse_starting_items(line: &str, monkey_id: MonkeyId) -> Vec<Item> {
        line.trim()
            .strip_prefix("Starting items: ")
            .unwrap()
            .split(", ")
            .enumerate()
            .map(|(idx, value)| Item {
                // No monkeys have over 10 starting items, so these will be unique
                id: monkey_id * 10 + idx,
                value: value.parse::<isize>().unwrap(),
            })
            .collect()
    }

    fn parse_operation(line: &'a str) -> Operation {
        Operation(
            match line
                .trim()
                .strip_prefix("Operation: new = old ")
                .unwrap()
                .split(" ")
                .collect::<Vec<_>>()[..]
            {
                ["+", "old"] => Box::new(|x| x + x),
                ["*", "old"] => Box::new(|x| x * x),
                ["+", operand] => {
                    let operand = operand.parse::<isize>().unwrap();
                    Box::new(move |x| x + operand)
                }
                ["*", operand] => {
                    let operand = operand.parse::<isize>().unwrap();
                    Box::new(move |x| x * operand)
                }
                _ => panic!("Could not parse operation line: {line}"),
            },
        )
    }

    fn parse_test_modulo(line: &str) -> isize {
        line.trim()
            .strip_prefix("Test: divisible by ")
            .unwrap()
            .parse()
            .unwrap()
    }

    fn parse_true_dest(line: &str) -> MonkeyId {
        line.trim()
            .strip_prefix("If true: throw to monkey ")
            .unwrap()
            .parse()
            .unwrap()
    }

    fn parse_false_dest(line: &str) -> MonkeyId {
        line.trim()
            .strip_prefix("If false: throw to monkey ")
            .unwrap()
            .parse()
            .unwrap()
    }

    // Compute the new value of the item and target monkey
    fn inspect(&self, item: Item, include_worry: bool) -> (Item, MonkeyId) {
        // Apply operation and (maybe) worry division
        let new_value: isize = self.operation.0.as_ref()(item.value);
        let new_value = if include_worry {
            new_value / 3
        } else {
            new_value
        };

        // Apply the test function and determine a destination monkey
        let dest_monkey = if new_value % self.test_modulo == 0 {
            self.true_dest
        } else {
            self.false_dest
        };

        (
            Item {
                id: item.id,
                value: new_value,
            },
            dest_monkey,
        )
    }
}

#[derive(Debug)]
struct State {
    // ith vector is items held by monkey i
    items: Vec<Vec<Item>>,
    // ith element is number of inspections by ith monkey
    inspections: Vec<usize>,
    // Determine whether to divide by 3 after operation
    include_worry: bool,
    // Use this modulo to keep sizes limited when not using worry, doesn't change result
    safe_modulo: isize,
}

impl State {
    fn new(monkeys: &Vec<Monkey>, include_worry: bool) -> Self {
        State {
            items: monkeys
                .iter()
                .map(|monkey| monkey.starting_items.clone())
                .collect(),
            inspections: vec![0; monkeys.len()],
            include_worry,
            safe_modulo: monkeys
                .iter()
                .map(|monkey| monkey.test_modulo)
                .product::<isize>(),
        }
    }

    fn execute_round(&mut self, monkeys: &Vec<Monkey>) {
        for monkey in monkeys {
            self.execute_turn(monkey);
        }
    }

    fn execute_turn(&mut self, monkey: &Monkey) {
        // Get all the items for this turn
        let items = self.items[monkey.id].clone();
        self.items[monkey.id].clear();

        // Process the items one by one
        for item in items {
            self.inspections[monkey.id] += 1;

            let (mut new_item, dest_monkey) = monkey.inspect(item, self.include_worry);

            // Note: this trick does not make sense if we're using worry
            // This is because modulo is not closed under division
            if !self.include_worry {
                new_item.value = new_item.value % self.safe_modulo;
            }

            self.items[dest_monkey].push(new_item);
        }
    }

    fn get_monkey_business(&self) -> usize {
        let mut inspections = self.inspections.clone();
        inspections.sort_by_key(|x| Reverse(*x));
        inspections[0] * inspections[1]
    }
}

fn parse_input(input: &str) -> Vec<Monkey> {
    input
        .split("\n\n")
        .map(|text| Monkey::parse(text))
        .collect()
}

fn part1(input: &str) -> String {
    let monkeys = parse_input(input);
    let mut state = State::new(&monkeys, true);

    for _ in 0..20 {
        state.execute_round(&monkeys);
    }

    state.get_monkey_business().to_string()
}

fn part2(input: &str) -> String {
    let monkeys = parse_input(input);
    let mut state = State::new(&monkeys, false);

    for _ in 0..10000 {
        state.execute_round(&monkeys)
    }

    state.get_monkey_business().to_string()
}

pub fn run(input: &str) {
    println!("Solution to part 1: {}", part1(input));
    println!("Solution to part 2: {}", part2(input));
}
