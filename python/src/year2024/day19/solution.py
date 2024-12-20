def parse_input(puzzle_input: str) -> tuple[set[str], list[str]]:
    """Returns set of available words and the list of goal patterns"""
    word_line, _, *goal_patterns = puzzle_input.split("\n")
    words = set(word_line.split(", "))
    return words, goal_patterns


def get_num_partitions(goal: str, words: set[str], memo: dict[str, int]) -> int:
    if goal in memo:
        return memo[goal]

    if not goal:
        return 1

    num_partitions = 0
    for word in words:
        if goal.startswith(word):
            num_partitions += get_num_partitions(goal[len(word) :], words, memo)

    memo[goal] = num_partitions
    return num_partitions


def part_1(puzzle_input: str) -> str | int:
    words, goals = parse_input(puzzle_input)
    memo: dict[str, int] = {}
    return sum(1 for goal in goals if get_num_partitions(goal, words, memo))


def part_2(puzzle_input: str) -> str | int:
    words, goals = parse_input(puzzle_input)
    memo: dict[str, int] = {}
    return sum(get_num_partitions(goal, words, memo) for goal in goals)
