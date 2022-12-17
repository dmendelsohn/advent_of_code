from pathlib import Path
from typing import List, Optional

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"

INVERSES = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}
INVERSES.update({v: k for (k, v) in INVERSES.items()})


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_input(use_test_input: bool = False) -> List[str]:
    raw_input = read_input(use_test_input)
    return raw_input.split("\n")


def get_invalid_char(line: str) -> Optional[str]:
    stack = []
    for char in line:
        if char in "({[<":
            stack.append(char)
        elif char in INVERSES:
            if stack.pop() != INVERSES[char]:
                return char
        else:
            raise ValueError(f"Invalid char {char}")
    return None  # Incomplete expression


def part_1(use_test_input: bool = False) -> str:
    lines = parse_input(use_test_input)
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    total = 0
    for line in lines:
        invalid_char = get_invalid_char(line)
        if invalid_char:
            total += scores[invalid_char]
    return f"{total}"


def get_completion_seq(line: str) -> Optional[str]:
    stack = []
    for char in line:
        if char in "({[<":
            stack.append(char)
        elif char in INVERSES:
            if stack.pop() != INVERSES[char]:
                return None  # Invalid rather than incomplete
        else:
            raise ValueError(f"Invalid char {char}")

    # Reverse stack and invert each character
    return "".join(INVERSES[char] for char in stack[::-1])


def score_seq(seq: str) -> int:
    scores = {")": 1, "]": 2, "}": 3, ">": 4}
    total = 0
    for char in seq:
        total *= 5
        total += scores[char]
    return total


def part_2(use_test_input: bool = False) -> str:
    lines = parse_input(use_test_input)
    scores = []
    for line in lines:
        completion_seq = get_completion_seq(line)
        if completion_seq:
            scores.append(score_seq(completion_seq))
    if len(scores) % 2 == 0:
        raise ValueError("Even number of input lines is not allowed")
    median = sorted(scores)[len(scores) // 2]
    return str(median)
