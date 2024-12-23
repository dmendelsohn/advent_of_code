from collections import defaultdict
from typing import DefaultDict

MODULO = 2**24


def get_next_secret(secret: int) -> int:
    secret = (secret ^ (secret << 6)) % MODULO
    secret = (secret ^ (secret >> 5)) % MODULO
    secret = (secret ^ (secret << 11)) % MODULO
    return secret


def process_secret(secret: int, bananas: DefaultDict[tuple[int, ...], int]) -> None:
    seen: set[tuple[int, ...]] = set()
    diffs: list[int] = []
    for _ in range(2000):
        next_secret = get_next_secret(secret)
        diffs.append(next_secret % 10 - secret % 10)
        diffs = diffs[-4:]  # Up to last for elements
        if len(diffs) == 4:
            diff_seq_key = tuple(diffs)
            if diff_seq_key not in seen:
                bananas[diff_seq_key] += next_secret % 10
                seen.add(diff_seq_key)
        secret = next_secret


def part_1(puzzle_input: str) -> str | int:
    total = 0
    for secret in map(int, puzzle_input.split("\n")):
        for _ in range(2000):
            secret = get_next_secret(secret)
        total += secret
    return total


def part_2(puzzle_input: str) -> str | int:
    bananas: DefaultDict[tuple[int, ...], int] = defaultdict(int)
    for secret in map(int, puzzle_input.split("\n")):
        process_secret(secret, bananas)
    return max(bananas.values())
