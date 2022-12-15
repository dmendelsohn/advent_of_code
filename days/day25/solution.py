from pathlib import Path
from typing import List

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"

Grid = List[List[str]]


def print_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))
    print("")


def shift_row(grid: Grid, r: int) -> int:
    num_moves = 0
    can_wrap = grid[r][0] == "."
    c = 0
    while c < len(grid[0]) - 1:
        if grid[r][c] == ">" and grid[r][c+1] == ".":
            num_moves += 1
            grid[r][c] = "."
            grid[r][c+1] = ">"
            c += 1
        c += 1
    if c == len(grid[0]) - 1 and grid[r][-1] == ">" and can_wrap:
        num_moves += 1
        grid[r][-1] = "."
        grid[r][0] = ">"
    return num_moves


def shift_col(grid: Grid, c: int) -> int:
    num_moves = 0
    can_wrap = grid[0][c] == "."
    r = 0
    while r < len(grid) - 1:
        if grid[r][c] == "v" and grid[r+1][c] == ".":
            num_moves += 1
            grid[r][c] = "."
            grid[r+1][c] = "v"
            r += 1
        r += 1
    if r == len(grid) - 1 and grid[-1][c] == "v" and can_wrap:
        num_moves += 1
        grid[-1][c] = "."
        grid[0][c] = "v"
    return num_moves


def perform_step(grid: Grid) -> int:
    num_moves = 0
    for r in range(len(grid)):
        num_moves += shift_row(grid, r)
    for c in range(len(grid[0])):
        num_moves += shift_col(grid, c)
    return num_moves


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_input(use_test_input: bool = False) -> Grid:
    raw_input = read_input(use_test_input)
    return [list(line.strip()) for line in raw_input.split("\n")]


def part_1(use_test_input: bool = False) -> str:
    grid = parse_input(use_test_input)
    num_steps = 0
    while True:
        num_steps += 1
        num_moves = perform_step(grid)
        if num_moves == 0:
            break
    return f"{num_steps}"


def part_2(use_test_input: bool = False) -> str:
    grid = parse_input(use_test_input)
    pass
