from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from enum import IntEnum
from functools import total_ordering
from typing import DefaultDict, cast

from typing_extensions import Self


class HandType(IntEnum):
    HIGH = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_KIND = 3
    FULL_HOUSE = 4
    FOUR_KIND = 5
    FIVE_KIND = 6

    @classmethod
    def from_card_freqs(cls, card_freqs: Iterable[int]) -> "HandType":
        match sorted(card_freqs):
            case [1, 1, 1, 1, 1]:
                return HandType.HIGH
            case [1, 1, 1, 2]:
                return HandType.PAIR
            case [1, 2, 2]:
                return HandType.TWO_PAIR
            case [1, 1, 3]:
                return HandType.THREE_KIND
            case [2, 3]:
                return HandType.FULL_HOUSE
            case [1, 4]:
                return HandType.FOUR_KIND
            case [5]:
                return HandType.FIVE_KIND
            case _:
                raise ValueError(f"Could not categorize hand with frequencies: {card_freqs}")


@total_ordering
@dataclass
class BaseHand(ABC):
    cards: tuple[str, str, str, str, str]
    bid: int

    @property
    @abstractmethod
    def hand_type(self) -> HandType:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_card_order() -> str:
        raise NotImplementedError

    def __lt__(self, other: "BaseHand") -> bool:
        # Guard against instances of different subclasses being compared
        if type(self) != type(other):
            raise ValueError(f"Cannot compare {type(self)} to {type(other)}")

        if self.hand_type < other.hand_type:
            return True
        if self.hand_type > other.hand_type:
            return False

        # Fall back on looking at each card
        card_order = self.get_card_order()
        for self_card, other_card in zip(self.cards, other.cards):
            if card_order.index(self_card) < card_order.index(other_card):
                return True
            if card_order.index(self_card) > card_order.index(other_card):
                return False

        return False

    def __str__(self) -> str:
        return f"{''.join(self.cards)} {int(self.bid)}"

    @classmethod
    def from_line(cls, line: str) -> Self:
        card_part, bid_part = line.split()
        cards = cast(tuple[str, str, str, str, str], tuple(card_part))
        return cls(cards, int(bid_part))


class SimpleHand(BaseHand):
    @property
    def hand_type(self) -> HandType:
        card_freqs: DefaultDict[str, int] = defaultdict(int)
        for card in self.cards:
            card_freqs[card] += 1

        return HandType.from_card_freqs(card_freqs.values())

    @staticmethod
    def get_card_order() -> str:
        return "23456789TJQKA"


class JokerHand(BaseHand):
    @property
    def hand_type(self) -> HandType:
        card_freqs: DefaultDict[str, int] = defaultdict(int)
        for card in self.cards:
            card_freqs[card] += 1

        joker_count = card_freqs.pop("J", 0)
        if card_freqs:
            most_common = max(card_freqs.items(), key=lambda item: item[1])[0]
        else:
            # Special case: all cards were jokers
            most_common = "J"

        card_freqs[most_common] += joker_count

        return HandType.from_card_freqs(card_freqs.values())

    @staticmethod
    def get_card_order() -> str:
        return "J23456789TQKA"


def part_1(puzzle_input: str) -> str | int:
    hands = sorted(SimpleHand.from_line(line) for line in puzzle_input.split("\n"))
    return sum((idx + 1) * hand.bid for idx, hand in enumerate(hands))


def part_2(puzzle_input: str) -> str | int:
    hands = sorted(JokerHand.from_line(line) for line in puzzle_input.split("\n"))
    return sum((idx + 1) * hand.bid for idx, hand in enumerate(hands))
