from pathlib import Path
from typing import List, NamedTuple

INPUT_PATH = Path(__file__).parent / "input.txt"


class Command(NamedTuple):
    direction: str
    distance: int


def parse_line(line: str) -> Command:
    parts = line.strip().split()
    return Command(parts[0], int(parts[1]))


def parse_input() -> List[Command]:
    lines = open(INPUT_PATH).read().strip().split("\n")
    return [parse_line(line) for line in lines]


def part_1() -> str:
    commands = parse_input()
    horiz = depth = 0
    for command in commands:
        if command.direction == "forward":
            horiz += command.distance
        elif command.direction == "down":
            depth += command.distance
        elif command.direction == "up":
            depth -= command.distance
        else:
            raise ValueError(f"Unknown direction: {command.direction}")
    print(f"horiz={horiz}, depth={depth}")
    return f"{horiz * depth}"


def part_2() -> str:
    commands = parse_input()
    horiz = depth = aim = 0
    for command in commands:
        if command.direction == "forward":
            horiz += command.distance
            depth += aim * command.distance
        elif command.direction == "down":
            aim += command.distance
        elif command.direction == "up":
            aim -= command.distance
        else:
            raise ValueError(f"Unknown direction: {command.direction}")
    print(f"horiz={horiz}, depth={depth}")
    return f"{horiz * depth}"
