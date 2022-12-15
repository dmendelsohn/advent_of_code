from pathlib import Path
from statistics import mean, median
from typing import List

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_input(use_test_input: bool = False) -> List[int]:
    raw_input = read_input(use_test_input)
    return [int(elt) for elt in raw_input.split(",")]


def get_cost(positions: List[int], target: int) -> int:
    return sum(abs(pos - target) for pos in positions)


def get_cost_2(positions: List[int], target: int) -> int:
    cost = 0
    for pos in positions:
        n = abs(pos - target)
        cost += n * (n + 1) // 2
    return cost


def part_1(use_test_input: bool = False) -> str:
    positions = parse_input(use_test_input)
    print(positions)
    target = round(median(positions))
    print(target)
    cost = get_cost(positions, target)
    print(f"Moving to {target} would cost {cost}")
    return f"{cost}"


def part_2(use_test_input: bool = False) -> str:
    positions = parse_input(use_test_input)
    # Try the number right below and right above the mean
    lo_target = int(mean(positions))
    hi_target = lo_target + 1
    lo_cost = get_cost_2(positions, lo_target)
    hi_cost = get_cost_2(positions, hi_target)
    if lo_cost < hi_cost:
        cost, target = lo_cost, lo_target
    else:
        cost, target = hi_cost, hi_target
    print(f"Moving to {target} would cost {cost}")
    return f"{cost}"
