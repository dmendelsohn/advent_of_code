import functools
import math
from collections import defaultdict
from typing import DefaultDict


def get_initial_frequencies(puzzle_input: str) -> DefaultDict[int, int]:
    freqs: DefaultDict[int, int] = defaultdict(int)
    for num in map(int, puzzle_input.split()):
        freqs[num] += 1
    return freqs


@functools.cache
def transform(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif (num_digits := int(math.log10(stone)) + 1) % 2 == 0:
        return list(divmod(stone, 10 ** (num_digits // 2)))
    else:
        return [2024 * stone]


def blink(stone_freqs: DefaultDict[int, int]) -> DefaultDict[int, int]:
    result: DefaultDict[int, int] = defaultdict(int)
    for num, freq in stone_freqs.items():
        for transform_num in transform(num):
            result[transform_num] += freq
    return result


def part_1(puzzle_input: str) -> str | int:
    stones = get_initial_frequencies(puzzle_input)
    for _ in range(25):
        stones = blink(stones)
    return sum(freq for freq in stones.values())


def part_2(puzzle_input: str) -> str | int:
    stones = get_initial_frequencies(puzzle_input)
    for _ in range(75):
        stones = blink(stones)
    return sum(freq for freq in stones.values())
