import math
from enum import Enum, IntEnum, auto
from typing import NamedTuple


class Direction(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def rotate(self, num_turns: int) -> "Direction":
        """Rotate a certain number of 90 degree clockwise turns"""
        return Direction((self + num_turns) % 4)


class Action(Enum):
    MOVE = auto()
    TURN = auto()


class Instruction(NamedTuple):
    action: Action
    # Units for turns are 90 degree increments clockwise
    amount: int


def parse_instructions(text: str) -> list[Instruction]:
    output = []
    idx = 0
    while idx < len(text):
        if text[idx] == "R":
            output.append(Instruction(Action.TURN, 1))
            idx += 1
        elif text[idx] == "L":
            output.append(Instruction(Action.TURN, 3))
            idx += 1
        else:
            num_str = ""
            while idx < len(text) and text[idx].isdigit():
                num_str += text[idx]
                idx += 1
            output.append(Instruction(Action.MOVE, int(num_str)))
    return output


class Location(NamedTuple):
    row: int
    col: int

    def neighbor(self, direction: Direction) -> "Location":
        match direction:
            case Direction.RIGHT:
                row_offset, col_offset = 0, 1
            case Direction.DOWN:
                row_offset, col_offset = 1, 0
            case Direction.LEFT:
                row_offset, col_offset = 0, -1
            case Direction.UP:
                row_offset, col_offset = -1, 0
            case _:
                raise ValueError(f"Unrecognized {direction=}")

        return Location(self.row + row_offset, self.col + col_offset)


class Edge(NamedTuple):
    start_loc: Location
    direction: Direction
    length: int


class Stitch(NamedTuple):
    edge_1: Edge
    direction_1: Direction
    edge_2: Edge
    direction_2: Direction


class Cell(Enum):
    EMPTY = " "
    OPEN = "."
    WALL = "#"


class Grid:
    def __init__(self, text: str, *, is_part_2: bool):
        # Raw input, splitting each char into an individual string
        self._grid: list[list[Cell]] = []
        self._jumps: dict[tuple[Location, Direction], tuple[Location, Direction]] = {}

        lines = text.split("\n")
        num_cols = max(len(line) for line in lines)
        for line in lines:
            # Update the grid
            new_row = [Cell(char) for char in line]
            padding = num_cols - len(new_row)
            assert padding >= 0
            new_row.extend([Cell.EMPTY] * padding)
            self._grid.append(new_row)

        # Initialize the side_length property
        num_cells = sum(sum(1 for cell in row if cell != Cell.EMPTY) for row in self._grid)
        self._cube_side_length = math.isqrt(num_cells // 6)
        assert 6 * self._cube_side_length**2 == num_cells

        # Set up overflow jumps for each row
        if is_part_2:
            self._setup_part2_overflow()
        else:
            self._setup_basic_overflow()

    def _setup_basic_overflow(self) -> None:
        for row in range(len(self._grid)):
            min_filled_loc = Location(
                row=row,
                col=next(
                    col for col in range(len(self._grid[0])) if self._grid[row][col] != Cell.EMPTY
                ),
            )
            max_filled_loc = Location(
                row=row,
                col=next(
                    col
                    for col in range(len(self._grid[0]) - 1, -1, -1)
                    if self._grid[row][col] != Cell.EMPTY
                ),
            )
            self._jumps[min_filled_loc, Direction.LEFT] = (max_filled_loc, Direction.LEFT)
            self._jumps[max_filled_loc, Direction.RIGHT] = (min_filled_loc, Direction.RIGHT)

        # Set up overflow jumps for each column
        for col in range(len(self._grid[0])):
            min_filled_loc = Location(
                row=next(
                    row for row in range(len(self._grid)) if self._grid[row][col] != Cell.EMPTY
                ),
                col=col,
            )
            max_filled_loc = Location(
                row=next(
                    row
                    for row in range(len(self._grid) - 1, -1, -1)
                    if self._grid[row][col] != Cell.EMPTY
                ),
                col=col,
            )
            self._jumps[min_filled_loc, Direction.UP] = (max_filled_loc, Direction.UP)
            self._jumps[max_filled_loc, Direction.DOWN] = (min_filled_loc, Direction.DOWN)

    def _setup_part2_overflow(self) -> None:
        # Our approach here is to use a hard-coded math of stitched edges
        # I didn't want to bother with the logic of calculating how the folding works
        side_length = self.cube_side_length
        if side_length == 4:
            stitches = {
                Stitch(
                    edge_1=Edge(start_loc=Location(0, 8), direction=Direction.RIGHT, length=4),
                    direction_1=Direction.UP,
                    edge_2=Edge(start_loc=Location(4, 3), direction=Direction.LEFT, length=4),
                    direction_2=Direction.UP,
                ),
                Stitch(
                    edge_1=Edge(start_loc=Location(0, 8), direction=Direction.DOWN, length=4),
                    direction_1=Direction.LEFT,
                    edge_2=Edge(start_loc=Location(4, 4), direction=Direction.RIGHT, length=4),
                    direction_2=Direction.UP,
                ),
                Stitch(
                    edge_1=Edge(start_loc=Location(0, 11), direction=Direction.DOWN, length=4),
                    direction_1=Direction.RIGHT,
                    edge_2=Edge(start_loc=Location(11, 15), direction=Direction.UP, length=4),
                    direction_2=Direction.RIGHT,
                ),
                Stitch(
                    edge_1=Edge(start_loc=Location(4, 0), direction=Direction.DOWN, length=4),
                    direction_1=Direction.LEFT,
                    edge_2=Edge(start_loc=Location(11, 15), direction=Direction.LEFT, length=4),
                    direction_2=Direction.DOWN,
                ),
                Stitch(
                    edge_1=Edge(start_loc=Location(4, 11), direction=Direction.DOWN, length=4),
                    direction_1=Direction.RIGHT,
                    edge_2=Edge(start_loc=Location(8, 15), direction=Direction.LEFT, length=4),
                    direction_2=Direction.UP,
                ),
                Stitch(
                    edge_1=Edge(start_loc=Location(7, 0), direction=Direction.RIGHT, length=4),
                    direction_1=Direction.DOWN,
                    edge_2=Edge(start_loc=Location(11, 11), direction=Direction.LEFT, length=4),
                    direction_2=Direction.DOWN,
                ),
                Stitch(
                    edge_1=Edge(start_loc=Location(7, 4), direction=Direction.RIGHT, length=4),
                    direction_1=Direction.DOWN,
                    edge_2=Edge(start_loc=Location(11, 8), direction=Direction.UP, length=4),
                    direction_2=Direction.LEFT,
                ),
            }
        elif side_length == 50:
            stitches = {
                Stitch(
                    edge_1=Edge(start_loc=Location(0, 50), direction=Direction.RIGHT, length=50),
                    direction_1=Direction.UP,
                    edge_2=Edge(start_loc=Location(150, 0), direction=Direction.DOWN, length=50),
                    direction_2=Direction.LEFT,
                ),
                Stitch(
                    edge_1=Edge(start_loc=Location(0, 100), direction=Direction.RIGHT, length=50),
                    direction_1=Direction.UP,
                    #
                    edge_2=Edge(start_loc=Location(199, 0), direction=Direction.RIGHT, length=50),
                    direction_2=Direction.DOWN,
                ),
                Stitch(
                    edge_1=Edge(start_loc=Location(0, 50), direction=Direction.DOWN, length=50),
                    direction_1=Direction.LEFT,
                    edge_2=Edge(start_loc=Location(149, 0), direction=Direction.UP, length=50),
                    direction_2=Direction.LEFT,
                ),
                #
                Stitch(
                    edge_1=Edge(start_loc=Location(0, 149), direction=Direction.DOWN, length=50),
                    direction_1=Direction.RIGHT,
                    edge_2=Edge(start_loc=Location(149, 99), direction=Direction.UP, length=50),
                    direction_2=Direction.RIGHT,
                ),
                Stitch(
                    edge_1=Edge(start_loc=Location(50, 50), direction=Direction.DOWN, length=50),
                    direction_1=Direction.LEFT,
                    edge_2=Edge(start_loc=Location(100, 0), direction=Direction.RIGHT, length=50),
                    direction_2=Direction.UP,
                ),
                Stitch(
                    edge_1=Edge(start_loc=Location(50, 99), direction=Direction.DOWN, length=50),
                    direction_1=Direction.RIGHT,
                    edge_2=Edge(start_loc=Location(49, 100), direction=Direction.RIGHT, length=50),
                    direction_2=Direction.DOWN,
                ),
                Stitch(
                    edge_1=Edge(start_loc=Location(150, 49), direction=Direction.DOWN, length=50),
                    direction_1=Direction.RIGHT,
                    edge_2=Edge(start_loc=Location(149, 50), direction=Direction.RIGHT, length=50),
                    direction_2=Direction.DOWN,
                ),
            }
        else:
            raise NotImplementedError

        self._setup_overflow_with_stitches(stitches)

    def _setup_overflow_with_stitches(self, stitches: set[Stitch]):
        for stitch in stitches:
            assert stitch.edge_1.length == stitch.edge_2.length
            loc_1 = stitch.edge_1.start_loc
            loc_2 = stitch.edge_2.start_loc
            for _ in range(stitch.edge_1.length):
                # Set up the jump and its return jump
                self._jumps[loc_1, stitch.direction_1] = (loc_2, stitch.direction_2.rotate(2))
                self._jumps[loc_2, stitch.direction_2] = (
                    loc_1,
                    stitch.direction_1.rotate(2),
                )
                # Walk one location along the edge
                loc_1 = loc_1.neighbor(stitch.edge_1.direction)
                loc_2 = loc_2.neighbor(stitch.edge_2.direction)

    @property
    def cube_side_length(self) -> int:
        return self._cube_side_length

    def top_left(self) -> Location:
        return Location(
            row=0,
            col=next(col for col in range(len(self._grid[0])) if self._grid[0][col] != Cell.EMPTY),
        )

    def next_location(self, location: Location, direction: Direction) -> tuple[Location, Direction]:
        if (location, direction) in self._jumps:
            return self._jumps[location, direction]
        neighbor = location.neighbor(direction)
        if not self._is_open_or_wall(neighbor):
            raise RuntimeError(f"Stepped out of bounds from {location}: {direction=}")
        return neighbor, direction

    def next_location_if_open(
        self, loc: Location, direction: Direction
    ) -> tuple[Location, Direction]:
        next_loc, next_dir = self.next_location(loc, direction)
        return (
            (next_loc, next_dir)
            if self._grid[next_loc.row][next_loc.col] == Cell.OPEN
            else (loc, direction)
        )

    def _is_open_or_wall(self, loc: Location) -> bool:
        if (
            loc.row < 0
            or loc.col < 0
            or loc.row >= len(self._grid)
            or loc.col >= len(self._grid[0])
        ):
            return False
        return self._grid[loc.row][loc.col] != Cell.EMPTY


def parse_input(puzzle_input: str, *, is_part_2: bool) -> tuple[Grid, list[Instruction]]:
    grid_text, instruction_text = puzzle_input.split("\n\n")
    return Grid(grid_text, is_part_2=is_part_2), parse_instructions(instruction_text)


def follow_path(
    grid: Grid, loc: Location, facing: Direction, instructions: list[Instruction]
) -> tuple[Location, Direction]:
    for instruction in instructions:
        if instruction.action == Action.MOVE:
            for _ in range(instruction.amount):
                loc, facing = grid.next_location_if_open(loc, facing)
        elif instruction.action == Action.TURN:
            facing = facing.rotate(instruction.amount)
        else:
            raise ValueError(f"Unrecognized {instruction.action=}")
    return loc, facing


def part_1(puzzle_input: str) -> str | int:
    grid, instructions = parse_input(puzzle_input, is_part_2=False)
    end_location, end_facing = follow_path(grid, grid.top_left(), Direction.RIGHT, instructions)
    return 1000 * (end_location.row + 1) + 4 * (end_location.col + 1) + end_facing


def part_2(puzzle_input: str) -> str | int:
    grid, instructions = parse_input(puzzle_input, is_part_2=True)
    end_location, end_facing = follow_path(grid, grid.top_left(), Direction.RIGHT, instructions)
    return 1000 * (end_location.row + 1) + 4 * (end_location.col + 1) + end_facing
