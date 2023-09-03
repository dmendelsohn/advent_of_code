from collections import deque
from enum import Enum
from typing import NamedTuple


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class Point(NamedTuple):
    row: int
    col: int


START = Point(0, 1)


class Blizzard(NamedTuple):
    location: Point
    direction: Direction


def parse_input(text: str) -> tuple[set[Blizzard], int, int]:
    """Return the blizzards, the max row we can visit, and the max col we can visit"""
    lines = text.split("\n")
    max_row = len(lines) - 2  # Minus two because last row is inaccessible
    max_col = len(lines[0]) - 2  # Minus two because last col is inaccessible
    blizzards = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            point = Point(row, col)
            match char:
                case "<":
                    blizzards.add(Blizzard(point, Direction.LEFT))
                case ">":
                    blizzards.add(Blizzard(point, Direction.RIGHT))
                case "v":
                    blizzards.add(Blizzard(point, Direction.DOWN))
                case "^":
                    blizzards.add(Blizzard(point, Direction.UP))
                case ".":
                    # Open space, not a blizzard
                    pass
                case "#":
                    # Wall, not a blizzard
                    pass
                case _:
                    raise ValueError(f"Unexpected input {char=}")

    return blizzards, max_row, max_col


class Forecast:
    """Class to lazily compute the forecast as far out as we need"""

    def __init__(self, initial_blizzards: set[Blizzard], *, max_row: int, max_col: int):
        # self._blizzards represents state after self._num_steps
        self._blizzards = initial_blizzards
        self._num_steps = 0

        self._min_row = 1
        self._max_row = max_row
        self._min_col = 1
        self._max_col = max_col
        self._start = Point(self._min_row - 1, self._min_col)
        self._end = Point(self._max_row + 1, self._max_col)

        # Tracks what forecasted free spots exist: elements are (location, time)
        self._free_spots: set[tuple[Point, int]] = set()
        self._record_free_spots()

    def _record_free_spots(self) -> None:
        # Start by finding all spots (including the start and end)
        free_spots = {self._start, self._end}
        for row in range(self._min_row, self._max_row + 1):
            for col in range(self._min_col, self._max_col + 1):
                free_spots.add(Point(row, col))

        # Now remove all the spots that are not actually free
        for blizzard in self._blizzards:
            if blizzard.location in free_spots:
                free_spots.remove(blizzard.location)

        # Now update the stored free spots
        for spot in free_spots:
            self._free_spots.add((spot, self._num_steps))

    def _next_blizzard(self, blizzard: Blizzard) -> Blizzard:
        next_row = blizzard.location.row + blizzard.direction.value[0]
        if next_row < self._min_row:
            next_row = self._max_row
        elif next_row > self._max_row:
            next_row = self._min_row

        next_col = blizzard.location.col + blizzard.direction.value[1]
        if next_col < self._min_col:
            next_col = self._max_col
        elif next_col > self._max_col:
            next_col = self._min_col

        return Blizzard(Point(next_row, next_col), blizzard.direction)

    def _next_step(self) -> None:
        self._blizzards = {self._next_blizzard(blizzard) for blizzard in self._blizzards}
        self._num_steps += 1
        self._record_free_spots()

    def _is_in_bounds(self, point: Point) -> bool:
        if point in (self._start, self._end):
            return True
        return (
            self._min_row <= point.row <= self._max_row
            and self._min_col <= point.col <= self._max_col
        )

    def is_free(self, point: Point, time: int) -> bool:
        if not self._is_in_bounds(point):
            return False

        while self._num_steps < time:
            self._next_step()

        return (point, time) in self._free_spots


def get_path_length(start: Point, end: Point, start_time: int, forecast: Forecast) -> int:
    queue = deque([(start, start_time)])
    seen = {(start, start_time)}
    while queue:
        location, time = queue.popleft()
        time += 1
        neighbors = [location] + [
            Point(location.row + direction.value[0], location.col + direction.value[1])
            for direction in Direction
        ]
        for neighbor in neighbors:
            if neighbor == end:
                return time

            node = (neighbor, time)
            if node in seen:
                continue
            else:
                seen.add(node)

            if forecast.is_free(neighbor, time):
                queue.append(node)

    raise RuntimeError("Could not find any path")


def part_1(puzzle_input: str) -> str | int:
    blizzards, max_row, max_col = parse_input(puzzle_input)
    start = Point(0, 1)
    end = Point(max_row + 1, max_col)
    forecast = Forecast(blizzards, max_row=max_row, max_col=max_col)
    return get_path_length(start, end, 0, forecast)


def part_2(puzzle_input: str) -> str | int:
    blizzards, max_row, max_col = parse_input(puzzle_input)
    start = Point(0, 1)
    end = Point(max_row + 1, max_col)
    forecast = Forecast(blizzards, max_row=max_row, max_col=max_col)

    first_leg_time = get_path_length(start, end, 0, forecast)
    second_leg_time = get_path_length(end, start, first_leg_time, forecast)
    return get_path_length(start, end, second_leg_time, forecast)
