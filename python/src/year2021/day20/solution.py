from pathlib import Path
from typing import List, NamedTuple, Set, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"

Pattern = List[bool]


class Point(NamedTuple):
    x: int
    y: int


class Box(NamedTuple):
    x_min: int
    y_min: int
    x_len: int
    y_len: int

    @property
    def x_max(self) -> int:
        return self.x_min + self.x_len

    @property
    def y_max(self) -> int:
        return self.y_min + self.y_len


class Board(NamedTuple):
    background_state: bool
    points: Set[Point]

    @property
    def bounding_box(self) -> Box:
        """Bounding box includes a border of width one"""
        x_min = min(p.x for p in self.points) - 1
        x_max = max(p.x for p in self.points) + 1
        y_min = min(p.y for p in self.points) - 1
        y_max = max(p.y for p in self.points) + 1
        return Box(x_min, y_min, x_max - x_min, y_max - y_min)

    @property
    def num_lit(self) -> int:
        if self.background_state:
            raise ValueError("Infinite lit")
        else:
            return len(self.points)

    def __str__(self) -> str:
        box = self.bounding_box
        lines = []
        for y in range(box.y_min, box.y_max + 1):
            present_char, absent_char = (".", "#") if self.background_state else ("#", ".")
            line = "".join(
                present_char if Point(x, y) in self.points else absent_char
                for x in range(box.x_min, box.x_max + 1)
            )
            lines.append(line)
        lines.append(f"Background is {'#' if self.background_state else '.'}")
        lines.append(f"Anchor is ({box.x_min}, {box.y_min})")
        lines.append("")
        return "\n".join(lines)


def get_pattern_index(board: Board, point: Point) -> int:
    binary_str = ""
    for y in range(point.y - 1, point.y + 2):
        for x in range(point.x - 1, point.x + 2):
            state = (
                board.background_state
                if Point(x, y) not in board.points
                else not board.background_state
            )
            binary_str += str(int(state))
    return int(binary_str, 2)


def get_next_board(board: Board, pattern: Pattern) -> Board:
    next_background_state = pattern[-1] if board.background_state else pattern[0]
    box = board.bounding_box
    next_points = set()
    for y in range(box.y_min, box.y_max + 1):
        for x in range(box.x_min, box.x_max + 1):
            point = Point(x, y)
            pattern_index = get_pattern_index(board, point)
            next_state = pattern[pattern_index]
            if next_state != next_background_state:
                next_points.add(point)
    return Board(background_state=next_background_state, points=next_points)


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_input(use_test_input: bool = False) -> Tuple[Board, Pattern]:
    raw_input = read_input(use_test_input)
    lines = raw_input.split("\n")
    pattern = [char == "#" for char in lines.pop(0).strip()]
    y = 0
    points = set()
    for line in lines:
        line = line.strip()
        if not line:
            continue  # Skip blank lines
        points.update(Point(idx, y) for idx, char in enumerate(line) if char == "#")
        y += 1
    return Board(background_state=False, points=points), pattern


def part_1(use_test_input: bool = False) -> str:
    board, pattern = parse_input(use_test_input)
    for _ in range(2):
        board = get_next_board(board, pattern)
    return f"{board.num_lit}"


def part_2(use_test_input: bool = False) -> str:
    board, pattern = parse_input(use_test_input)
    for _ in range(50):
        board = get_next_board(board, pattern)
    return f"{board.num_lit}"
