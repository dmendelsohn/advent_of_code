from pathlib import Path
from typing import List

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"


class Octopus:
    def __init__(self, count: int = 0, has_flashed: bool = False):
        self.count = count
        self.has_flashed = has_flashed


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_input(use_test_input: bool = False) -> List[List[Octopus]]:
    raw_input = read_input(use_test_input)
    return [[Octopus(int(c), False) for c in line.strip()] for line in raw_input.split("\n")]


def do_flashes(grid: List[List[Octopus]]) -> int:
    """
    Modifies the grid and returns the number of flashes
    Flashes any octopus that is ready to flash, and increases all its neighbors
    """
    num_flashes = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col].count > 9 and not grid[row][col].has_flashed:
                grid[row][col].has_flashed = True
                num_flashes += 1
                for row_offset in range(-1, 2):
                    for col_offset in range(-1, 2):
                        row_adj, col_adj = row + row_offset, col + col_offset
                        if 0 <= row_adj < len(grid) and 0 <= col_adj < len(grid[0]):
                            if row_offset != 0 or col_offset != 0:
                                grid[row_adj][col_adj].count += 1
    return num_flashes


def reset_flashes(grid: List[List[Octopus]]) -> None:
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            grid[row][col].has_flashed = False
            if grid[row][col].count > 9:
                grid[row][col].count = 0


def do_step(grid: List[List[Octopus]]) -> int:
    """Modifies the grid and returns total number of flashes"""
    num_flashes = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            grid[row][col].count += 1
    while True:
        num_new_flashes = do_flashes(grid)
        if num_new_flashes:
            num_flashes += num_new_flashes
        else:
            break

    reset_flashes(grid)
    return num_flashes


def part_1(use_test_input: bool = False) -> str:
    grid = parse_input(use_test_input)
    total_flashes = 0
    for _ in range(100):
        total_flashes += do_step(grid)
    return f"{total_flashes}"


def part_2(use_test_input: bool = False) -> str:
    grid = parse_input(use_test_input)
    step_num = 0
    while True:
        step_num += 1
        flashes = do_step(grid)
        if flashes == len(grid) * len(grid[0]):
            break
    return f"{step_num}"
