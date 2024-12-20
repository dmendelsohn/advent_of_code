from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from typing import DefaultDict


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)


@dataclass
class Maze:
    grid: list[list[bool]]  # True when there is a wall, False otherwise
    start: Vector
    end: Vector

    def __str__(self) -> str:
        lines: list[str] = []
        for y, row in enumerate(self.grid):
            line: list[str] = []
            for x, is_wall in enumerate(row):
                if is_wall:
                    line.append("#")
                elif Vector(x, y) == self.start:
                    line.append("S")
                elif Vector(x, y) == self.end:
                    line.append("E")
                else:
                    line.append(".")
            lines.append("".join(line))
        return "\n".join(lines)

    def is_empty(self, pos: Vector) -> bool:
        return (
            0 <= pos.x < len(self.grid[0])
            and 0 <= pos.y < len(self.grid)
            and not self.grid[pos.y][pos.x]
        )

    def get_path(self) -> list[Vector]:
        """Get the one path through the maze, including start and end locations"""
        path: list[Vector] = [self.start]
        seen: set[Vector] = {self.start}
        while (last := path[-1]) != self.end:
            for offset in (Vector(1, 0), Vector(0, 1), Vector(-1, 0), Vector(0, -1)):
                neighbor = last + offset
                if neighbor not in seen and self.is_empty(neighbor):
                    seen.add(neighbor)
                    path.append(neighbor)
                    break
        return path

    def get_possible_cheat_ends(self, cheat_start: Vector, max_dist: int) -> Iterator[Vector]:
        for x_offset in range(-max_dist, max_dist + 1):
            for y_offset in range(-max_dist + abs(x_offset), max_dist - abs(x_offset) + 1):
                if self.is_empty(cheat_end := cheat_start + Vector(x_offset, y_offset)):
                    yield cheat_end

    def count_cheats(
        self,
        cheat_start: Vector,
        max_cheat_duration: int,
        dist_from_end: dict[Vector, int],
        num_cheats_by_time_save: DefaultDict[int, int],
    ) -> None:
        """Count cheats keyed by time save"""
        for cheat_end in self.get_possible_cheat_ends(cheat_start, max_cheat_duration):
            cheat_length = abs(cheat_start.x - cheat_end.x) + abs(cheat_start.y - cheat_end.y)
            if (
                time_save := dist_from_end[cheat_end] - dist_from_end[cheat_start] - cheat_length
            ) > 0:
                num_cheats_by_time_save[time_save] += 1


def parse_input(puzzle_input: str) -> Maze:
    grid: list[list[bool]] = []
    start: Vector | None = None
    end: Vector | None = None
    for y, line in enumerate(puzzle_input.split("\n")):
        row = []
        for x, char in enumerate(line):
            if char == "S":
                start = Vector(x, y)
            elif char == "E":
                end = Vector(x, y)

            row.append(char == "#")
        grid.append(row)

    assert start is not None
    assert end is not None
    return Maze(grid, start, end)


def part_1(puzzle_input: str) -> str | int:
    maze = parse_input(puzzle_input)
    path = maze.get_path()
    dist_from_end = {pos: len(path) - idx - 1 for idx, pos in enumerate(path)}
    num_cheats_by_time_save: DefaultDict[int, int] = defaultdict(int)
    for pos in path:
        maze.count_cheats(pos, 2, dist_from_end, num_cheats_by_time_save)

    # print(num_cheats_by_time_save)  # For debugging the example where the answer is 0
    return sum(
        num_cheats for time_save, num_cheats in num_cheats_by_time_save.items() if time_save >= 100
    )


def part_2(puzzle_input: str) -> str | int:
    maze = parse_input(puzzle_input)
    path = maze.get_path()
    dist_from_end = {pos: len(path) - idx - 1 for idx, pos in enumerate(path)}
    num_cheats_by_time_save: DefaultDict[int, int] = defaultdict(int)
    for pos in path:
        maze.count_cheats(pos, 20, dist_from_end, num_cheats_by_time_save)

    # print(num_cheats_by_time_save)  # For debugging the example where the answer is 0
    return sum(
        num_cheats for time_save, num_cheats in num_cheats_by_time_save.items() if time_save >= 100
    )
