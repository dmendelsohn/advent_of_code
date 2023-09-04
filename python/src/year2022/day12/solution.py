from collections import deque
from typing import NamedTuple


class Location(NamedTuple):
    row: int
    col: int


def get_height(char: str) -> int:
    if char == "S":
        char = "a"
    elif char == "E":
        char = "z"
    return ord(char) - ord("a")


def parse_input(text: str) -> tuple[list[list[str]], Location, Location]:
    """Return the grid and the locations of the start and end"""
    grid = []
    start = end = None
    for row, line in enumerate(text.split("\n")):
        grid.append(list(line))
        for col, char in enumerate(line):
            if char == "S":
                start = Location(row, col)
            elif char == "E":
                end = Location(row, col)

    assert start is not None
    assert end is not None
    return grid, start, end


def get_distance(grid: list[list[str]], start: Location, end_chars: str) -> int:
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        current, distance = queue.popleft()
        distance += 1
        height = get_height(grid[current.row][current.col])
        for row_offset, col_offset in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            neighbor = Location(current.row + row_offset, current.col + col_offset)
            if neighbor in seen:
                continue

            if 0 <= neighbor.row < len(grid) and 0 <= neighbor.col < len(grid[0]):
                neighbor_char = grid[neighbor.row][neighbor.col]
                if get_height(neighbor_char) >= height - 1:
                    if neighbor_char in end_chars:
                        return distance
                    queue.append((neighbor, distance))
                    seen.add(neighbor)

    raise RuntimeError("Could not find path")


def part_1(puzzle_input: str) -> str | int:
    grid, start, end = parse_input(puzzle_input)
    return get_distance(grid, end, "S")


def part_2(puzzle_input: str) -> str | int:
    grid, start, end = parse_input(puzzle_input)
    return get_distance(grid, end, "Sa")
