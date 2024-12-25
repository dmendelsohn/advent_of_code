import itertools
from dataclasses import dataclass

from typing_extensions import Self


@dataclass
class Schematic:
    is_lock: bool
    heights: list[int]

    @classmethod
    def parse(cls, text: str) -> Self:
        lines = text.split("\n")
        is_lock = lines[0][0] == "#"
        heights: list[int] = []
        for col in range(len(lines[0])):
            height = 0
            while lines[height + 1 if is_lock else -height - 2][col] == "#":
                height += 1
            heights.append(height)
        return cls(is_lock, heights)


def is_possible_match(lock: Schematic, key: Schematic) -> bool:
    return all(sum(pair) <= 5 for pair in zip(lock.heights, key.heights))


def part_1(puzzle_input: str) -> str | int:
    locks: list[Schematic] = []
    keys: list[Schematic] = []
    for section in puzzle_input.split("\n\n"):
        if (schematic := Schematic.parse(section)).is_lock:
            locks.append(schematic)
        else:
            keys.append(schematic)

    return sum(1 for pair in itertools.product(locks, keys) if is_possible_match(*pair))


def part_2(_: str) -> str | int:
    return "N/A"
