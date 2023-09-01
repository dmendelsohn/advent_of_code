DECRYPTION_KEY = 811589153


def parse_input(puzzle_input: str, multiplier: int = 1) -> list[tuple[int, int]]:
    # Outputs are (elt, index with elements == elt)
    seen: dict[int, int] = {}
    output = []
    for elt in map(int, puzzle_input.split("\n")):
        index = seen.get(elt, -1) + 1
        seen[elt] = index
        output.append((elt * multiplier, index))
    return output


def mix(mutable: list[tuple[int, int]], elt: tuple[int, int]) -> None:
    start_index = mutable.index(elt)
    offset = elt[0] % (len(mutable) - 1)
    target_index = start_index + offset
    if target_index >= len(mutable):
        # Add one on wraparound because the wrap itself does not skip any elements
        target_index = (target_index % len(mutable)) + 1

    mutable.pop(start_index)
    mutable.insert(target_index, elt)


def get_answer(mutable: list[tuple[int, int]]) -> int:
    result = 0
    start_index = mutable.index((0, 0))
    for index in (1000, 2000, 3000):
        result += mutable[(start_index + index) % len(mutable)][0]
    return result


def part_1(puzzle_input: str) -> str | int:
    original = parse_input(puzzle_input)
    mutable = original.copy()
    for elt in original:
        mix(mutable, elt)

    return get_answer(mutable)


def part_2(puzzle_input: str) -> str | int:
    original = parse_input(puzzle_input, DECRYPTION_KEY)
    mutable = original.copy()
    for _ in range(10):
        for elt in original:
            mix(mutable, elt)

    return get_answer(mutable)
