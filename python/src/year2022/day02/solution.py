from enum import Enum


class Shape(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6


def parse_input(text: str) -> list[tuple[str, str]]:
    return [(line[0], line[2]) for line in text.split("\n")]


def get_result(you: Shape, other: Shape) -> Result:
    diff = (you.value - other.value) % 3
    if diff == 0:
        return Result.DRAW
    elif diff == 1:
        return Result.WIN
    else:
        return Result.LOSS


def part_1(puzzle_input: str) -> str | int:
    total = 0
    for other_char, you_char in parse_input(puzzle_input):
        other = {"A": Shape.ROCK, "B": Shape.PAPER, "C": Shape.SCISSORS}[other_char]
        you = {"X": Shape.ROCK, "Y": Shape.PAPER, "Z": Shape.SCISSORS}[you_char]
        result = get_result(you, other)
        total += result.value
        total += you.value
    return total


def get_you(other: Shape, result: Result) -> Shape:
    if result == Result.WIN:
        val = other.value + 1
        if val == 4:
            val = 1
        return Shape(val)
    elif result == Result.LOSS:
        val = other.value - 1
        if val == 0:
            val = 3
        return Shape(val)
    else:
        return other


def part_2(puzzle_input: str) -> str | int:
    total = 0
    for other_char, result_char in parse_input(puzzle_input):
        other = {"A": Shape.ROCK, "B": Shape.PAPER, "C": Shape.SCISSORS}[other_char]
        result = {"X": Result.LOSS, "Y": Result.DRAW, "Z": Result.WIN}[result_char]
        you = get_you(other, result)
        total += result.value
        total += you.value
    return total
