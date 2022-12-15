from pathlib import Path
from typing import List

INPUT_PATH = Path(__file__).parent / "input.txt"


def get_input_ints() -> List[int]:
    lines = open(INPUT_PATH).read().strip().split("\n")
    return [int(line) for line in lines]


def part_1() -> str:
    depths = get_input_ints()
    num_inc = 0
    for i in range(1, len(depths)):
        if depths[i] > depths[i-1]:
            num_inc += 1
    return str(num_inc)


def part_2() -> str:
    depths = get_input_ints()
    num_inc = 0
    for i in range(3, len(depths)):
        if depths[i] > depths[i-3]:
            num_inc += 1
    return str(num_inc)
