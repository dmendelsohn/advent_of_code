def parse_input(puzzle_input: str) -> list[list[int]]:
    return [[int(part) for part in line.split()] for line in puzzle_input.split("\n")]


def get_iterative_diffs(sequence: list[int]) -> list[list[int]]:
    iterative_diffs: list[list[int]] = [sequence[:]]
    while any(elt != 0 for elt in iterative_diffs[-1]):
        # Calculate another level of diff sequences
        diffs: list[int] = []
        for idx in range(len(iterative_diffs[-1]) - 1):
            diffs.append(iterative_diffs[-1][idx + 1] - iterative_diffs[-1][idx])
        iterative_diffs.append(diffs)

    return iterative_diffs


def extrapolate_right(sequence: list[int]) -> int:
    iterative_diffs = get_iterative_diffs(sequence)
    return sum(diffs[-1] for diffs in iterative_diffs)


def extrapolate_left(sequence: list[int]) -> int:
    iterative_diffs = get_iterative_diffs(sequence)
    new_value = 0
    for diffs in reversed(iterative_diffs):
        new_value = diffs[0] - new_value
    return new_value


def part_1(puzzle_input: str) -> str | int:
    sequences = parse_input(puzzle_input)
    return sum(extrapolate_right(seq) for seq in sequences)


def part_2(puzzle_input: str) -> str | int:
    sequences = parse_input(puzzle_input)
    return sum(extrapolate_left(seq) for seq in sequences)
