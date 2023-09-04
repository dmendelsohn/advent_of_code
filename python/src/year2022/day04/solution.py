from typing import NamedTuple


class Range(NamedTuple):
    """Inclusive int range"""

    low: int
    high: int

    @classmethod
    def parse(cls, text: str) -> "Range":
        low, high = map(int, text.split("-"))
        return Range(low, high)

    def contains(self, other: "Range") -> bool:
        return self.low <= other.low and self.high >= other.high

    def overlaps(self, other: "Range") -> bool:
        return max(self.low, other.low) <= min(self.high, other.high)


def parse_input(text: str) -> list[tuple[Range, Range]]:
    pairs = []
    for line in text.split("\n"):
        first_range, second_range = line.split(",")
        pairs.append((Range.parse(first_range), Range.parse(second_range)))
    return pairs


def part_1(puzzle_input: str) -> str | int:
    pairs = parse_input(puzzle_input)
    return sum(1 for first, second in pairs if first.contains(second) or second.contains(first))


def part_2(puzzle_input: str) -> str | int:
    pairs = parse_input(puzzle_input)
    return sum(1 for first, second in pairs if first.overlaps(second))
