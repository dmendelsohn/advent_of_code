import itertools
import math
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def reduce(self) -> "Vector":
        gcd = math.gcd(self.x, self.y)
        return Vector(self.x // gcd, self.y // gcd)


def parse_input(input: str) -> tuple[Vector, dict[str, set[Vector]]]:
    """
    Return
    - max location (last row, last col)
    - map of symbols to attenna locations
    """
    antennae: DefaultDict[str, set[Vector]] = defaultdict(set)
    lines = input.split("\n")
    for row, line in enumerate(lines):
        for col, symbol in enumerate(line):
            if symbol != ".":
                antennae[symbol].add(Vector(col, row))
    max_row = len(lines) - 1
    max_col = len(lines[0]) - 1
    return (Vector(max_col, max_row), dict(antennae))


def is_in_bounds(node: Vector, max_location: Vector) -> bool:
    return 0 <= node.x <= max_location.x and 0 <= node.y <= max_location.y


def get_antinodes_part_1(nodes: set[Vector], max_location: Vector) -> set[Vector]:
    antinodes: set[Vector] = set()
    for node_pair in itertools.combinations(nodes, 2):
        diff = node_pair[1] - node_pair[0]
        if is_in_bounds(antinode := node_pair[1] + diff, max_location):
            antinodes.add(antinode)
        if is_in_bounds(antinode := node_pair[0] - diff, max_location):
            antinodes.add(antinode)
    return antinodes


def part_1(puzzle_input: str) -> str | int:
    max_location, antennae = parse_input(puzzle_input)
    antinodes: set[Vector] = set()
    for nodes in antennae.values():
        antinodes.update(get_antinodes_part_1(nodes, max_location))
    return len(antinodes)


def get_antinodes_part_2(nodes: set[Vector], max_location: Vector) -> set[Vector]:
    antinodes: set[Vector] = set()
    for node_pair in itertools.combinations(nodes, 2):
        diff = (node_pair[1] - node_pair[0]).reduce()

        # Go forward
        antinode = node_pair[0]
        while is_in_bounds(antinode, max_location):
            antinodes.add(antinode)
            antinode += diff

        # Go backward
        antinode = node_pair[0]
        while is_in_bounds(antinode, max_location):
            antinodes.add(antinode)
            antinode -= diff

    return antinodes


def part_2(puzzle_input: str) -> str | int:
    max_location, antennae = parse_input(puzzle_input)
    antinodes: set[Vector] = set()
    for nodes in antennae.values():
        antinodes.update(get_antinodes_part_2(nodes, max_location))
    return len(antinodes)
