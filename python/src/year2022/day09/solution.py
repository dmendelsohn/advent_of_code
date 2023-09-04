from enum import Enum
from typing import NamedTuple


class Location(NamedTuple):
    row: int
    col: int


class Direction(Enum):
    RIGHT = (0, 1)
    LEFT = (0, -1)
    UP = (-1, 0)
    DOWN = (1, 0)


def parse_line(line: str) -> tuple[Direction, int]:
    dir_str, mag_str = line.split()
    for direction in Direction:
        if direction.name[0] == dir_str:
            return direction, int(mag_str)
    raise ValueError(f"Could not parse {line=}")


def parse_input(text: str) -> list[tuple[Direction, int]]:
    return [parse_line(line) for line in text.split("\n")]


class Snake:
    def __init__(self, num_knots: int):
        self._knots = [Location(0, 0)] * num_knots
        self._visited_by_tail = {Location(0, 0)}  # Set of locations visited by tail

    @staticmethod
    def _increment_toward_zero(num: int) -> int:
        if num == 0:
            return 0
        elif num > 0:
            return num - 1
        else:
            return num + 1

    @classmethod
    def _follow(cls, tail: Location, head: Location) -> Location:
        row_offset, col_offset = head.row - tail.row, head.col - tail.col
        if abs(row_offset) <= 1 and abs(col_offset) <= 1:
            # No need to move
            return tail

        def get_movement(num: int) -> int:
            if num == 0:
                return 0
            else:
                return num // abs(num)

        return Location(
            tail.row + get_movement(row_offset),
            tail.col + get_movement(col_offset),
        )

    def _step(self, direction: Direction) -> None:
        # Move the head in the indicated direction
        self._knots[0] = Location(
            self._knots[0].row + direction.value[0], self._knots[0].col + direction.value[1]
        )

        # Move each subsequent not toward its predecessor
        for i in range(1, len(self._knots)):
            self._knots[i] = self._follow(self._knots[i], self._knots[i - 1])

        self._visited_by_tail.add(self._knots[-1])

    def execute_instructions(self, instructions: list[tuple[Direction, int]]):
        for direction, amount in instructions:
            for _ in range(amount):
                self._step(direction)

    @property
    def num_visited_by_tail(self) -> int:
        return len(self._visited_by_tail)


def part_1(puzzle_input: str) -> str | int:
    instructions = parse_input(puzzle_input)
    snake = Snake(2)
    snake.execute_instructions(instructions)
    return snake.num_visited_by_tail


def part_2(puzzle_input: str) -> str | int:
    instructions = parse_input(puzzle_input)
    snake = Snake(10)
    snake.execute_instructions(instructions)
    return snake.num_visited_by_tail
