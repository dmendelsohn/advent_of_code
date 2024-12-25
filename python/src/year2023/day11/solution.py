import itertools
from dataclasses import dataclass
from functools import cached_property

from typing_extensions import Self


@dataclass(frozen=True)
class Position:
    row: int
    col: int


@dataclass(frozen=True)
class Universe:
    galaxies: frozenset[Position]

    @classmethod
    def parse(cls, text: str) -> Self:
        galaxies: set[Position] = set()
        for row, line in enumerate(text.split("\n")):
            for col, char in enumerate(line):
                if char == "#":
                    galaxies.add(Position(row, col))
        return cls(frozenset(galaxies))

    @cached_property
    def expanded_rows(self) -> list[int]:
        occupied_rows = {galaxy.row for galaxy in self.galaxies}
        return [
            row for row in range(min(occupied_rows), max(occupied_rows)) if row not in occupied_rows
        ]

    @cached_property
    def expanded_cols(self) -> list[int]:
        occupied_cols = {galaxy.col for galaxy in self.galaxies}
        return [
            col for col in range(min(occupied_cols), max(occupied_cols)) if col not in occupied_cols
        ]

    def get_expanded_distance(self, a: Position, b: Position, factor: int) -> int:
        return (
            sum(factor for row in self.expanded_rows if min(a.row, b.row) < row < max(a.row, b.row))
            + sum(
                factor for col in self.expanded_cols if min(a.col, b.col) < col < max(a.col, b.col)
            )
            + abs(b.row - a.row)
            + abs(b.col - a.col)
        )


def part_1(puzzle_input: str) -> str | int:
    universe = Universe.parse(puzzle_input)
    return sum(
        universe.get_expanded_distance(a, b, 1)
        for a, b in itertools.combinations(universe.galaxies, 2)
    )


def part_2(puzzle_input: str) -> str | int:
    universe = Universe.parse(puzzle_input)
    return sum(
        universe.get_expanded_distance(a, b, 10**6 - 1)
        for a, b in itertools.combinations(universe.galaxies, 2)
    )
