def parse_input(input: str) -> list[list[int]]:
    return [[int(num) for num in line.split()] for line in input.split("\n")]


def is_safe_part1(report: list[int], upward: bool, start_idx: int = 0) -> bool:
    for i in range(start_idx, len(report) - 1):
        delta = report[i + 1] - report[i]
        delta = delta if upward else -delta
        if delta < 1 or delta > 3:
            return False
    return True


def is_safe_part2(report: list[int], upward: bool) -> bool:
    delta_mult = 1 if upward else -1
    deltas = [(report[i + 1] - report[i]) * delta_mult for i in range(len(report) - 1)]
    bad_delta_indices: list[int] = []
    for idx, delta in enumerate(deltas):
        if delta < 1 or delta > 3:
            bad_delta_indices.append(idx)

    if len(bad_delta_indices) == 0:
        return True

    if len(bad_delta_indices) == 1:
        idx = bad_delta_indices[0]

        # If it's the first or last delta, we're good!
        if idx == 0 or idx == len(deltas) - 1:
            return True

        # See if it can be combined with prior delta
        if 1 <= deltas[idx] + deltas[idx - 1] <= 3:
            return True

        # See if it can be combined with next delta
        if 1 <= deltas[idx] + deltas[idx + 1] <= 3:
            return True

        # Can't do anything :(
        return False

    if len(bad_delta_indices) == 2:
        # Try to combine the deltas with each other
        lo_idx = bad_delta_indices[0]
        hi_idx = bad_delta_indices[1]
        if hi_idx - lo_idx == 1 and 1 <= deltas[lo_idx] + deltas[hi_idx] <= 3:
            return True

        # Can't do anything :(
        return False

    # More than 2 bad deltas
    return False


def part_1(puzzle_input: str) -> str | int:
    reports = parse_input(puzzle_input)
    return sum(
        1 for report in reports if is_safe_part1(report, True) or is_safe_part1(report, False)
    )


def part_2(puzzle_input: str) -> str | int:
    reports = parse_input(puzzle_input)
    return sum(
        1 for report in reports if is_safe_part2(report, True) or is_safe_part2(report, False)
    )
