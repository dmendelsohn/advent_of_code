def get_group_total(text: str) -> int:
    return sum(int(line) for line in text.split("\n"))


def get_group_totals(text: str) -> list[int]:
    return [get_group_total(group) for group in text.split("\n\n")]


def part_1(puzzle_input: str) -> str | int:
    return max(get_group_totals(puzzle_input))


def part_2(puzzle_input: str) -> str | int:
    return sum(sorted(get_group_totals(puzzle_input))[-3:])
