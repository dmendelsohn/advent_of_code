from dataclasses import dataclass
from functools import cache
from typing import Literal, TypeAlias, TypeVar


@dataclass(frozen=True)
class Vector:
    x: int
    y: int


class Position(Vector):
    def __add__(self, other: Vector) -> "Position":
        return Position(self.x + other.x, self.y + other.y)


class Movement(Vector):
    def __post_init__(self) -> None:
        if self.x**2 + self.y**2 != 1:
            raise ValueError(f"Movement {self} is not a valid unit vector")


ButtonT = TypeVar("ButtonT", int, Movement)
ActionT: TypeAlias = Literal["A"]


# Maps characters to their position on the number pad
NUMBER_PAD: dict[int | ActionT, Position] = {
    0: Position(1, 3),
    1: Position(0, 2),
    2: Position(1, 2),
    3: Position(2, 2),
    4: Position(0, 1),
    5: Position(1, 1),
    6: Position(2, 1),
    7: Position(0, 0),
    8: Position(1, 0),
    9: Position(2, 0),
    "A": Position(2, 3),
}

# Maps movements to their position on the keypad
ARROW_PAD: dict[Movement | ActionT, Position] = {
    Movement(1, 0): Position(2, 1),  # >
    Movement(0, 1): Position(1, 1),  # v
    Movement(-1, 0): Position(0, 1),  # <
    Movement(0, -1): Position(1, 0),  # ^
    "A": Position(2, 0),  # A
}


@cache
def get_movement_sequences(
    start: Position,
    end: Position,
    invalid_position: Position,
) -> set[tuple[Movement, ...]]:
    """
    Get all reasonable movement paths from the start to the end position, avoiding the
    invalid position.

    There are up to two reasonable paths:
    - moving horizontally before vertically
    - moving vertically before horizontally

    This function returns 1 element of length zero if the start and end position are the same
    This function returns 1 element if the start and end position are in the same row or column
    This function returns 1-2 elements if the start and end positions are diagonal
    """
    x_dist = end.x - start.x
    y_dist = end.y - start.y
    lateral_moves = (Movement(1 if x_dist >= 0 else -1, 0),) * abs(x_dist)
    vertical_moves = (Movement(0, 1 if y_dist >= 0 else -1),) * abs(y_dist)
    movement_sequences = {lateral_moves + vertical_moves, vertical_moves + lateral_moves}

    def is_valid_sequnce(movements: tuple[Movement, ...]) -> bool:
        current = start
        for movement in movements:
            current += movement
            if current == invalid_position:
                return False
        return True

    return {seq for seq in movement_sequences if is_valid_sequnce(seq)}


@cache
def get_min_moves(requested_buttons: tuple[ButtonT, ...], num_robots: int) -> int:
    """
    Calculate the minimum human presses to perform the requested button presses.
    Also include a final "A" press.
    We assume all robot arms start positioned at "A".
    """
    if not requested_buttons:
        # Just press "A"
        return 1

    pad: dict[ButtonT | ActionT, Position]
    if isinstance(requested_buttons[0], int):
        pad = NUMBER_PAD  # type: ignore[assignment]
        invalid_pos = Position(0, 3)
    else:
        pad = ARROW_PAD
        invalid_pos = Position(0, 0)

    buttons_to_press: list[ButtonT | Literal["A"]] = list(requested_buttons) + ["A"]
    if num_robots == 0:
        # Human is pressing the buttons directly
        return len(buttons_to_press)

    min_presses = 0
    for idx in range(len(buttons_to_press)):
        current_pos = pad[buttons_to_press[idx - 1]]
        next_pos = pad[buttons_to_press[idx]]
        min_presses += min(
            get_min_moves(movement_sequence, num_robots - 1)
            for movement_sequence in get_movement_sequences(current_pos, next_pos, invalid_pos)
        )

    return min_presses


def part_1(puzzle_input: str) -> str | int:
    total = 0
    for line in puzzle_input.split("\n"):
        assert line.endswith("A")
        numeric_value = int(line[:-1])
        sequence = tuple(map(int, line[:-1]))
        total += numeric_value * get_min_moves(sequence, 3)
    return total


def part_2(puzzle_input: str) -> str | int:
    total = 0
    for line in puzzle_input.split("\n"):
        assert line.endswith("A")
        numeric_value = int(line[:-1])
        sequence = tuple(map(int, line[:-1]))
        total += numeric_value * get_min_moves(sequence, 26)
    return total
