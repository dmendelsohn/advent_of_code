import operator
import re
from typing import Callable

Item = int
MonkeyId = int

LINE_REGEXES = [
    r"Monkey (\d+):",
    r"\s+Starting items: (.*)",
    r"\s+Operation: new = old ([\+\*]) (old|\d+)",
    r"\s+Test: divisible by (\d+)",
    r"\s+If true: throw to monkey (\d+)",
    r"\s+If false: throw to monkey (\d+)",
]


class Monkey:
    def __init__(
        self,
        monkey_id: MonkeyId,
        starting_items: list[Item],
        operation: Callable[[Item], Item],
        test_modulus: int,
        true_target: MonkeyId,
        false_target: MonkeyId,
    ):
        self._monkey_id = monkey_id
        self._items = starting_items.copy()
        self._operation = operation
        self._test_modulus = test_modulus
        self._true_target = true_target
        self._false_target = false_target
        self._num_thrown = 0

    def throw_items(self) -> list[tuple[Item, MonkeyId]]:
        """Returns the new value and target monkeys of all the thrown items"""
        result = [self._throw_item(item) for item in self._items]
        self._items.clear()
        self._num_thrown += len(result)
        return result

    def _throw_item(self, item: Item) -> tuple[Item, MonkeyId]:
        item = self._operation(item)
        if item % self._test_modulus == 0:
            return item, self._true_target
        else:
            return item, self._false_target

    def add_item(self, item: Item) -> None:
        self._items.append(item)

    def reduce_modulo(self, modulus: int) -> None:
        for idx in range(len(self._items)):
            self._items[idx] %= modulus

    @property
    def monkey_id(self) -> MonkeyId:
        return self._monkey_id

    @property
    def test_modulus(self) -> int:
        return self._test_modulus

    @property
    def num_thrown(self) -> int:
        return self._num_thrown

    @classmethod
    def parse(cls, text: str, *, is_part_2: bool) -> "Monkey":
        pattern = (
            r"Monkey (\d+):"
            r"\s+Starting items: (.*)"
            r"\s+Operation: new = old ([\+\*]) (old|\d+)"
            r"\s+Test: divisible by (\d+)"
            r"\s+If true: throw to monkey (\d+)"
            r"\s+If false: throw to monkey (\d+)"
        )
        match = re.match(pattern, text)
        if not match:
            raise ValueError(f"Could not parse {text=}")

        op = {"+": operator.add, "*": operator.mul}[match.groups()[2]]
        operand = match.groups()[3]

        def operation(x: int):
            val = op(x, x) if operand == "old" else op(x, int(operand))
            if not is_part_2:
                val //= 3
            return val

        return Monkey(
            monkey_id=int(match.groups()[0]),
            starting_items=[int(item) for item in match.groups()[1].split(", ")],
            operation=operation,
            test_modulus=int(match.groups()[4]),
            true_target=int(match.groups()[5]),
            false_target=int(match.groups()[6]),
        )


def parse_input(text: str, *, is_part_2: bool) -> list[Monkey]:
    monkeys = [Monkey.parse(block, is_part_2=is_part_2) for block in text.split("\n\n")]
    assert all(idx == monkey.monkey_id for idx, monkey in enumerate(monkeys))
    return monkeys


def do_round(monkeys: list[Monkey]) -> None:
    for monkey in monkeys:
        for item, target in monkey.throw_items():
            monkeys[target].add_item(item)


def multiply_two_most_active(monkeys: list[Monkey]) -> int:
    num_throws = sorted(monkey.num_thrown for monkey in monkeys)
    return num_throws[-1] * num_throws[-2]


def part_1(puzzle_input: str) -> str | int:
    monkeys = parse_input(puzzle_input, is_part_2=False)
    for _ in range(20):
        do_round(monkeys)
    return multiply_two_most_active(monkeys)


def part_2(puzzle_input: str) -> str | int:
    monkeys = parse_input(puzzle_input, is_part_2=True)

    # Trick: maintain items modulo (product-of-all-test-moduli)
    # We can do this because addition and multiplication are closed under the modulo operation
    total_modulus = 1
    for monkey in monkeys:
        total_modulus *= monkey.test_modulus

    for idx in range(10000):
        do_round(monkeys)
        for monkey in monkeys:
            monkey.reduce_modulo(total_modulus)

    return multiply_two_most_active(monkeys)
