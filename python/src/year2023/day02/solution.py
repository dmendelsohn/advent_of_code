import re
from dataclasses import dataclass
from typing import TypeAlias

# Maps colors to their frequencies
Sample: TypeAlias = dict[str, int]


@dataclass
class Game:
    identifier: int
    samples: list[Sample]

    @classmethod
    def from_line(cls, line: str) -> "Game":
        id_section, remainder = line.split(": ")
        if (id_match := re.search(r"Game (\d+)", id_section)) is None:
            raise ValueError(f"Could not parse ID section: {id_section}")
        identifier = int(id_match.groups()[0])

        samples: list[Sample] = []
        for sample_section in remainder.split("; "):
            sample: dict[str, int] = {}
            for clause in sample_section.split(", "):
                if (clause_match := re.search(r"(\d+) (\w+)", clause)) is None:
                    raise ValueError(f"Could not parse clause: '{clause}'")
                count = int(clause_match.groups()[0])
                color = clause_match.groups()[1]
                sample[color] = count
            samples.append(sample)

        return Game(identifier, samples)

    def is_possible(self, bag: Sample) -> bool:
        for sample in self.samples:
            for color, bag_count in bag.items():
                if sample.get(color, 0) > bag_count:
                    return False

        return True

    def get_smallest_bag(self) -> Sample:
        smallest_bag: Sample = {}
        for sample in self.samples:
            for color, count in sample.items():
                if count > smallest_bag.get(color, 0):
                    smallest_bag[color] = count
        return smallest_bag


def part_1(puzzle_input: str) -> str | int:
    games = [Game.from_line(line) for line in puzzle_input.split("\n")]
    ref_bag = {"red": 12, "green": 13, "blue": 14}
    return sum(game.identifier for game in games if game.is_possible(ref_bag))


def part_2(puzzle_input: str) -> str | int:
    games = [Game.from_line(line) for line in puzzle_input.split("\n")]
    total = 0
    for game in games:
        smallest_bag = game.get_smallest_bag()
        total += (
            smallest_bag.get("red", 0) * smallest_bag.get("green", 0) * smallest_bag.get("blue", 0)
        )
    return total
