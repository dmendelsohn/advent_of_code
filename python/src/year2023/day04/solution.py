import re
from dataclasses import dataclass


@dataclass
class Card:
    card_id: int
    card_numbers: set[int]
    winning_numbers: set[int]
    num_copies: int = 1

    @classmethod
    def from_line(cls, line) -> "Card":
        id_section, remainder = line.split(": ")
        if (id_match := re.search(r"Card +(\d+)", id_section)) is None:
            raise ValueError(f"Could not parse ID section: {id_section}")
        card_id = int(id_match.groups()[0])

        left, right = remainder.split(" | ")
        card_numbers = set(map(int, left.split()))
        winning_numbers = set(map(int, right.split()))
        return cls(card_id, card_numbers, winning_numbers)

    @property
    def num_overlap(self) -> int:
        return len(self.card_numbers & self.winning_numbers)

    @property
    def points(self) -> int:
        return 2 ** (self.num_overlap - 1) if self.num_overlap > 0 else 0


def part_1(puzzle_input: str) -> str | int:
    cards = [Card.from_line(line) for line in puzzle_input.split("\n")]
    return sum(card.points for card in cards)


def part_2(puzzle_input: str) -> str | int:
    cards = [Card.from_line(line) for line in puzzle_input.split("\n")]
    for idx, card in enumerate(cards):
        for offset in range(1, 1 + card.num_overlap):
            cards[idx + offset].num_copies += card.num_copies
    return sum(card.num_copies for card in cards)
