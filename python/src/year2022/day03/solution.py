def get_priority(char: str) -> int:
    if char == char.lower():
        return ord(char) - ord("a") + 1
    else:
        return ord(char) - ord("A") + 27


def get_halves(s: str) -> tuple[str, str]:
    if len(s) % 2 != 0:
        raise ValueError(f"Cannot split an odd-length string in half: {s}")
    return s[: len(s) // 2], s[len(s) // 2 :]


def part_1(puzzle_input: str) -> str | int:
    total_priority = 0
    for line in puzzle_input.split("\n"):
        first, second = get_halves(line)
        overlap = set(first).intersection(set(second))
        if len(overlap) != 1:
            raise ValueError(f"Unexpected {overlap=} for {line=}")
        total_priority += get_priority(overlap.pop())
    return total_priority


def part_2(puzzle_input: str) -> str | int:
    lines = puzzle_input.split("\n")
    if len(lines) % 3 != 0:
        raise ValueError(f"Need a multiple of 3 input lines, not {len(lines)}")

    total_priority = 0
    for idx in range(len(lines) // 3):
        overlap = (
            set(lines[3 * idx])
            .intersection(set(lines[3 * idx + 1]))
            .intersection(set(lines[3 * idx + 2]))
        )
        if len(overlap) != 1:
            raise ValueError(f"Unexpected {overlap=} for {idx=}")
        total_priority += get_priority(overlap.pop())
    return total_priority
