from collections import defaultdict
from typing import DefaultDict


def parse_input(input: str) -> tuple[list[int], list[int]]:
    """Return the left and right list"""
    left: list[int] = []
    right: list[int] = []
    for line in input.strip().split("\n"):
        parts = line.split()
        assert len(parts) == 2
        left.append(int(parts[0]))
        right.append(int(parts[1]))
    return left, right


def get_frequencies(nums: list[int]) -> DefaultDict[int, int]:
    freqs: DefaultDict[int, int] = defaultdict(int)
    for num in nums:
        freqs[num] += 1
    return freqs


def part_1(puzzle_input: str) -> str | int:
    left, right = parse_input(puzzle_input)
    left.sort()
    right.sort()
    diff = 0
    for left_elt, right_elt in zip(left, right):
        diff += abs(left_elt - right_elt)
    return diff


def part_2(puzzle_input: str) -> str | int:
    left, right = parse_input(puzzle_input)
    freqs = get_frequencies(right)
    total = 0
    for elt in left:
        total += elt * freqs[elt]
    return total
