import functools
import operator
import re
from typing import Callable, Optional

Monkeys = dict[str, str]

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
}


def parse_input(puzzle_input: str) -> Monkeys:
    monkeys = {}
    pattern = r"(\w+): (.*)"
    for line in puzzle_input.split("\n"):
        match = re.match(pattern, line)
        if not match:
            raise ValueError(f"Could not parse line: {line}")
        monkey, expression = match.groups()
        monkeys[monkey] = expression
    return monkeys


def make_cached_eval(monkeys: Monkeys, *, is_part_2: bool = False) -> Callable[[str], int]:
    @functools.cache
    def _cached_eval(monkey: str) -> int:
        expression = monkeys[monkey]
        if is_part_2 and monkey == "humn":
            raise ValueError("Cannot evaluate the human input")
        elif expression.isnumeric():
            return int(expression)
        else:
            pattern = r"(\w+) ([\+\-\*\/]) (\w+)"
            match = re.match(pattern, expression)
            if not match:
                raise ValueError(f"Invalid expression: {expression}")
            left_monkey, op, right_monkey = match.groups()
            left_val = _cached_eval(left_monkey)
            right_val = _cached_eval(right_monkey)
            return OPS[op](left_val, right_val)

    return _cached_eval


def safe_eval(monkey: str, cached_eval: Callable[[str], int]) -> Optional[int]:
    try:
        return cached_eval(monkey)
    except ValueError:
        return None


def solve(monkeys: Monkeys, monkey: str, value: int, cached_eval: Callable[[str], int]) -> int:
    """Return what humn would have to be to make cached_eval(monkey) = value"""
    if monkey == "humn":
        return value

    expr = monkeys[monkey]
    if expr.isnumeric():
        raise ValueError("Expected a variable equation to solve")

    left_root, op, right_root = monkeys[monkey].split()
    left_val = safe_eval(left_root, cached_eval)
    right_val = safe_eval(right_root, cached_eval)

    if left_val is None and right_val is None:
        raise NotImplementedError("Only one-sided variables equations are supported")
    if left_val is not None and right_val is not None:
        raise ValueError("Expected a one-sided variable equation to solve")

    if op == "+":
        if left_val is None and right_val is not None:
            return solve(monkeys, left_root, value - right_val, cached_eval)
        elif right_val is None and left_val is not None:
            return solve(monkeys, right_root, value - left_val, cached_eval)
        else:
            raise ValueError("Expected a one-sided variable equation to solve")
    elif op == "-":
        if left_val is None and right_val is not None:
            return solve(monkeys, left_root, value + right_val, cached_eval)
        elif right_val is None and left_val is not None:
            return solve(monkeys, right_root, left_val - value, cached_eval)
        else:
            raise ValueError("Expected a one-sided variable equation to solve")
    elif op == "*":
        if left_val is None and right_val is not None:
            return solve(monkeys, left_root, value // right_val, cached_eval)
        elif right_val is None and left_val is not None:
            return solve(monkeys, right_root, value // left_val, cached_eval)
        else:
            raise ValueError("Expected a one-sided variable equation to solve")
    elif op == "/":
        if left_val is None and right_val is not None:
            return solve(monkeys, left_root, value * right_val, cached_eval)
        elif right_val is None and left_val is not None:
            return solve(monkeys, right_root, left_val // value, cached_eval)
        else:
            raise ValueError("Expected a one-sided variable equation to solve")
    else:
        raise ValueError(f"Unrecognized operation: {op}")


def part_1(puzzle_input: str) -> str | int:
    monkeys = parse_input(puzzle_input)
    cached_eval = make_cached_eval(monkeys)
    return cached_eval("root")


def part_2(puzzle_input: str) -> str | int:
    monkeys = parse_input(puzzle_input)
    cached_eval = make_cached_eval(monkeys, is_part_2=True)

    left_root, _, right_root = monkeys["root"].split()
    left_val = safe_eval(left_root, cached_eval)
    right_val = safe_eval(right_root, cached_eval)

    if left_val is None:
        if right_val is None:
            raise NotImplementedError("Only one-sided variables equations are supported")
        return solve(monkeys, left_root, right_val, cached_eval)
    elif right_val is None:
        return solve(monkeys, right_root, left_val, cached_eval)
    else:
        raise ValueError("Expected at least one variable as a dependency of the root")
