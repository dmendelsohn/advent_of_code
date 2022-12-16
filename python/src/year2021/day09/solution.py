from pathlib import Path
from typing import FrozenSet, List, Set, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_input(use_test_input: bool = False) -> List[List[int]]:
    raw_input = read_input(use_test_input)
    return [[int(c) for c in line.strip()] for line in raw_input.split("\n")]


def is_low_point(grid: List[List[int]], row: int, col: int) -> bool:
    adjacent_nums = set()
    for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        adj_row = row + offset[0]
        adj_col = col + offset[1]
        if 0 <= adj_row < len(grid) and 0 <= adj_col < len(grid[0]):
            adjacent_nums.add(grid[adj_row][adj_col])
    return grid[row][col] < min(adjacent_nums)


def get_low_points(grid: List[List[int]]) -> Set[Tuple[int, int]]:
    low_points = set()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if is_low_point(grid, row, col):
                low_points.add((row, col))
    return low_points


def part_1(use_test_input: bool = False) -> str:
    grid = parse_input(use_test_input)
    low_points = get_low_points(grid)
    total = 0
    for low_point in low_points:
        risk_level = 1 + grid[low_point[0]][low_point[1]]
        total += risk_level
    return f"{total}"


def get_basin(
    grid: List[List[int]], row: int, col: int, visited_points: Set[Tuple[int, int]]
) -> Set[Tuple[int, int]]:
    """Get all points in basin that includes (row, col)"""
    # If location is visited, exit early, otherwise mark location as visited
    if (row, col) in visited_points:
        return set()
    else:
        visited_points.add((row, col))

    # Check of edge of basin
    if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]) or grid[row][col] == 9:
        return set()  # This point is not in the basin

    # Recursive call
    basin = {(row, col)}  # This point is in the basin
    for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        sub_basin = get_basin(grid, row + offset[0], col + offset[1], visited_points)
        basin.update(sub_basin)
    return basin


def get_all_basins(grid: List[List[int]]) -> Set[FrozenSet[Tuple[int, int]]]:
    basins = set()
    visited_points = set()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            basin = get_basin(grid, row, col, visited_points)
            # The basin can be empty if the point is already visited or has height 9
            if basin:
                basins.add(frozenset(basin))
    return basins


def get_score(basins: Set[FrozenSet[Tuple[int, int]]]) -> int:
    if len(basins) < 3:
        raise ValueError(f"Cannot get score when there are only {len(basins)} basins")
    basin_sizes = sorted([len(basin) for basin in basins], reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


def part_2(use_test_input: bool = False) -> str:
    grid = parse_input(use_test_input)
    basins = get_all_basins(grid)
    score = get_score(basins)
    return f"{score}"
