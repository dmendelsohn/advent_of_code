from typing import Any, NamedTuple


class Vector(NamedTuple):
    row: int
    col: int

    def __add__(self, other: Any) -> "Vector":
        if not isinstance(other, Vector):
            raise ValueError(f"Cannot add {other} to a Vector")
        return Vector(self.row + other.row, self.col + other.col)

    def __mul__(self, mul: Any) -> "Vector":
        if not isinstance(mul, int):
            raise ValueError(f"Cannot multiply a Vectory by {mul}")
        return Vector(mul * self.row, mul * self.col)


Grid = list[list[int]]


def parse_input(text: str) -> Grid:
    return [[int(char) for char in line] for line in text.split("\n")]


def view_toward(grid: Grid, start: Vector, direction: Vector) -> tuple[int, bool]:
    """Return number of trees (and whether the edge can be seen) along the given path"""
    start_height = grid[start.row][start.col]
    length = 1
    while True:
        other = start + direction * length
        if 0 <= other.row < len(grid) and 0 <= other.col < len(grid[0]):
            if grid[other.row][other.col] >= start_height:
                # We can see no further
                return length, False
            else:
                # Keep looking
                length += 1
        else:
            # We hit the edge
            return length - 1, True


def view(grid: Grid, start: Vector) -> tuple[int, bool]:
    """Return scenic score from a start point, and whether the edge can be seen"""
    can_see_edge = False
    scenic_score = 1
    for direction in [Vector(0, 1), Vector(1, 0), Vector(0, -1), Vector(-1, 0)]:
        _num_trees, _can_see_edge = view_toward(grid, start, direction)
        scenic_score *= _num_trees
        can_see_edge = can_see_edge or _can_see_edge
    return scenic_score, can_see_edge


def part_1(puzzle_input: str) -> str | int:
    grid = parse_input(puzzle_input)
    num_viewable_from_edge = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if view(grid, Vector(row, col))[1]:
                num_viewable_from_edge += 1
    return num_viewable_from_edge


def part_2(puzzle_input: str) -> str | int:
    grid = parse_input(puzzle_input)
    max_scenic_score = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            max_scenic_score = max(max_scenic_score, view(grid, Vector(row, col))[0])
    return max_scenic_score
