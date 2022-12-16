import re
from pathlib import Path
from typing import List, NamedTuple, Set, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"


class Point(NamedTuple):
    x: int
    y: int


class FoldInstruction(NamedTuple):
    axis: str
    fold_line: int


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_input(use_test_input: bool = False) -> Tuple[Set[Point], List[FoldInstruction]]:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    points = set()
    instructions = []
    with open(input_path) as f:
        while True:
            line = f.readline().strip()
            if line:
                x, y = [int(part) for part in line.split(",")]
                points.add(Point(x, y))
            else:
                break
        # After blank line, remaining lines are all instructions
        for line in f:
            pattern = "^fold along (.)=([0-9]+)$"
            match = re.match(pattern, line)
            if not match:
                raise RuntimeError(f"Invalid instruction line: {line}")
            axis, fold_line = match.groups()
            instructions.append(FoldInstruction(axis, int(fold_line)))
    return points, instructions


def fold(points: Set[Point], instruction: FoldInstruction) -> Set[Point]:
    new_points = set()
    for point in points:
        new_coords = {"x": point.x, "y": point.y}
        new_coords[instruction.axis] = min(
            new_coords[instruction.axis], 2 * instruction.fold_line - new_coords[instruction.axis]
        )
        new_points.add(Point(**new_coords))
    return new_points


def part_1(use_test_input: bool = False) -> str:
    points, instructions = parse_input(use_test_input)
    points = fold(points, instructions[0])
    return f"{len(points)}"


def render_points(points: Set[Point]) -> str:
    max_x = max(point.x for point in points)
    max_y = max(point.y for point in points)
    chars = []
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if Point(x, y) in points:
                chars.append("#")
            else:
                chars.append(".")
        chars.append("\n")
    return "".join(chars)


def part_2(use_test_input: bool = False) -> str:
    points, instructions = parse_input(use_test_input)
    for instruction in instructions:
        points = fold(points, instruction)
    return f"\n{render_points(points)}"
