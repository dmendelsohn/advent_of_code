from collections import defaultdict
from typing import DefaultDict


def get_range(text: str) -> tuple[int, int]:
    elts = [int(num) for num in text.split("-")]
    if len(elts) != 2:
        raise ValueError(f"Bad input: {text}")
    return elts[0], elts[1]


def get_digits(num: int) -> list[int]:
    if num < 0:
        raise ValueError("Negative numbers are not supported")
    elif num == 0:
        return [0]

    digits = []
    while num:
        digits.append(num % 10)
        num //= 10
    return list(reversed(digits))


def meets_criteria(num: int, with_part_2_restriction: bool = False) -> bool:
    digits = get_digits(num)
    if len(digits) != 6:
        return False

    for i in range(1, len(digits)):
        if digits[i - 1] > digits[i]:
            return False

    freqs: DefaultDict[int, int] = defaultdict(int)
    for digit in digits:
        freqs[digit] += 1

    has_dupe = any(freq > 1 for freq in freqs.values())
    if not has_dupe:
        return False

    has_exact_dupe = any(freq == 2 for freq in freqs.values())
    return not with_part_2_restriction or has_exact_dupe


def part_1(puzzle_input: str) -> str | int:
    range_min, range_max = get_range(puzzle_input)
    count = 0
    for num in range(range_min, 1 + range_max):
        if meets_criteria(num):
            count += 1
    return count


def part_2(puzzle_input: str) -> str | int:
    range_min, range_max = get_range(puzzle_input)
    count = 0
    for num in range(range_min, 1 + range_max):
        if meets_criteria(num, with_part_2_restriction=True):
            count += 1
    return count
