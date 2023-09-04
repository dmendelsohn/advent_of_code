def find_marker(s: str, n: int) -> int:
    return next(idx for idx in range(n, len(s)) if len(set(s[idx - n : idx])) == n)


def part_1(puzzle_input: str) -> str | int:
    return find_marker(puzzle_input, 4)


def part_2(puzzle_input: str) -> str | int:
    return find_marker(puzzle_input, 14)
