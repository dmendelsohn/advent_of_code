from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Deque

from typing_extensions import Self


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    @property
    def rot90(self) -> "Vector":
        """
        90 degree counterclockwise rotation
        Note that our y-axis is flipped (positive is downward)
        """
        return Vector(self.y, -self.x)


UNIT_VECTORS = (Vector(1, 0), Vector(0, 1), Vector(-1, 0), Vector(0, -1))


class Pipe(Enum):
    UP_DOWN = "|"
    LEFT_RIGHT = "-"
    UP_LEFT = "J"
    UP_RIGHT = "L"
    DOWN_LEFT = "7"
    DOWN_RIGHT = "F"

    def get_neighbors(self, position: Vector) -> set[Vector]:
        match self:
            case Pipe.UP_DOWN:
                offsets = {Vector(0, -1), Vector(0, 1)}
            case Pipe.LEFT_RIGHT:
                offsets = {Vector(-1, 0), Vector(1, 0)}
            case Pipe.UP_LEFT:
                offsets = {Vector(0, -1), Vector(-1, 0)}
            case Pipe.UP_RIGHT:
                offsets = {Vector(0, -1), Vector(1, 0)}
            case Pipe.DOWN_LEFT:
                offsets = {Vector(0, 1), Vector(-1, 0)}
            case Pipe.DOWN_RIGHT:
                offsets = {Vector(0, 1), Vector(1, 0)}

        return {position + offset for offset in offsets}


@dataclass
class Network:
    grid: list[list[Pipe | None]]
    start: Vector

    def __str__(self) -> str:
        lines: list[str] = []
        for y, row in enumerate(self.grid):
            line: list[str] = []
            for x, maybe_pipe in enumerate(row):
                if Vector(x, y) == self.start:
                    line.append("S")
                elif maybe_pipe is None:
                    line.append(".")
                else:
                    line.append(maybe_pipe.value)
            lines.append("".join(line))
        return "\n".join(lines)

    @classmethod
    def from_input(cls, puzzle_input: str) -> Self:
        # Note that the start location has a None value
        grid: list[list[Pipe | None]] = []
        start: Vector | None = None
        for y, line in enumerate(puzzle_input.split("\n")):
            row: list[Pipe | None] = []
            for x, char in enumerate(line):
                if char == "S":
                    assert start is None
                    start = Vector(x, y)
                    row.append(None)
                elif char == ".":
                    row.append(None)
                else:
                    row.append(Pipe(char))
            grid.append(row)

        assert start is not None
        return cls(grid, start)

    def is_in_bounds(self, position: Vector) -> bool:
        return 0 <= position.x < len(self.grid[0]) and 0 <= position.y < len(self.grid)

    def get_loop_start(self) -> Vector:
        possible_starts: list[Vector] = []
        for offset in UNIT_VECTORS:
            loop_start = self.start + offset
            if not self.is_in_bounds(loop_start):
                continue

            if (pipe := self.grid[loop_start.y][loop_start.x]) is None:
                continue

            if self.start not in pipe.get_neighbors(loop_start):
                # Doesn't connect
                continue

            possible_starts.append(loop_start)

        if not possible_starts:
            raise RuntimeError("Could not find a starting location for the loop")

        return possible_starts[0]

    def get_loop(self) -> list[Vector]:
        # First, find a neighbor where we can start following the loop
        path: list[Vector] = [self.start]
        path.append(self.get_loop_start())
        while True:
            current = path[-1]
            assert (pipe := self.grid[current.y][current.x]) is not None
            (next_position,) = {pos for pos in pipe.get_neighbors(current) if pos != path[-2]}
            if next_position == path[0]:
                break
            path.append(next_position)

        return path

    @staticmethod
    def is_left_handed(loop: list[Vector]) -> bool:
        """Returns whether the loop is a left handed loop"""
        net_left_turns: int = 0
        for idx in range(len(loop)):
            incoming_heading = loop[idx] - loop[idx - 1]
            outgoing_heading = loop[(idx + 1) % len(loop)] - loop[idx]
            if outgoing_heading == incoming_heading.rot90:
                net_left_turns += 1
            elif outgoing_heading == incoming_heading.rot90.rot90.rot90:
                net_left_turns -= 1

        if net_left_turns == 4:
            return True
        elif net_left_turns == -4:
            return False
        else:
            raise ValueError(f"Got unexpected {net_left_turns=}")

    def flood_fill(
        self, flood_start: Vector, filled: set[Vector], fill_boundary: set[Vector]
    ) -> None:
        """
        Flood fill without crossing fill boundary
        """
        if flood_start in fill_boundary or not self.is_in_bounds(flood_start):
            return

        filled.add(flood_start)
        queue: Deque[Vector] = deque([flood_start])
        while queue:
            position = queue.popleft()
            for offset in UNIT_VECTORS:
                neighbor = position + offset
                if neighbor in filled or neighbor in fill_boundary:
                    continue

                queue.append(neighbor)
                filled.add(neighbor)

    def get_enclosed_area(self, loop: list[Vector]) -> int:
        is_left_handed = self.is_left_handed(loop)
        filled: set[Vector] = set()
        fill_boundary = set(loop)
        for idx in range(len(loop)):
            current = loop[idx]
            incoming_heading = current - loop[idx - 1]
            inward_facing_normal = (
                incoming_heading.rot90 if is_left_handed else incoming_heading.rot90.rot90.rot90
            )
            self.flood_fill(current + inward_facing_normal, filled, fill_boundary)
        return len(filled)


def part_1(puzzle_input: str) -> str | int:
    network = Network.from_input(puzzle_input)
    loop = network.get_loop()
    return len(loop) // 2


def part_2(puzzle_input: str) -> str | int:
    network = Network.from_input(puzzle_input)
    loop = network.get_loop()
    return network.get_enclosed_area(loop)
