from dataclasses import dataclass
from enum import Enum

from typing_extensions import Self


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    @property
    def gps_coord(self) -> int:
        return 100 * self.y + self.x


class Direction(Enum):
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"
    UP = "^"

    @property
    def vector(self) -> Vector:
        match self:
            case Direction.RIGHT:
                return Vector(1, 0)
            case Direction.DOWN:
                return Vector(0, 1)
            case Direction.LEFT:
                return Vector(-1, 0)
            case Direction.UP:
                return Vector(0, -1)
            case _:
                raise ValueError(f"No vector for direction {self}")


@dataclass
class SimpleRoom:
    walls: set[Vector]
    boxes: set[Vector]
    robot: Vector

    def move_robot(self, direction: Direction) -> None:
        next_loc = self.robot + direction.vector

        next_empty_loc = next_loc
        while next_empty_loc in self.boxes:
            next_empty_loc += direction.vector

        if next_empty_loc in self.walls:
            # Cannot move
            return

        # If there is an adjacent box, move it to next_empty_loc
        if next_loc in self.boxes:
            self.boxes.remove(next_loc)
            self.boxes.add(next_empty_loc)

        self.robot = next_loc
        return

    @classmethod
    def from_str(cls, text: str) -> Self:
        # Initialize a room with a sentinel robot vector
        robot_sentinel = Vector(-1, -1)
        room = cls(set(), set(), robot_sentinel)
        for y, line in enumerate(text.split("\n")):
            for x, char in enumerate(line):
                match char:
                    case "#":
                        room.walls.add(Vector(x, y))
                    case "O":
                        room.boxes.add(Vector(x, y))
                    case "@":
                        if room.robot != robot_sentinel:
                            raise ValueError("Multiple robots in room")
                        room.robot = Vector(x, y)
        return room


@dataclass
class WideRoom:
    walls: set[Vector]
    boxes: set[Vector]  # Tracks left half of each box
    robot: Vector

    def _get_boxes_to_move(self, start: Vector, direction: Direction) -> set[Vector] | None:
        """
        Try to move the object at the start location if there is one.
        Return the set of boxes that would move.
        If we try to push a wall, return None.
        """
        if start in self.walls:
            return None

        left_of_start = start + Vector(-1, 0)
        if start in self.boxes or left_of_start in self.boxes:
            box = start if start in self.boxes else left_of_start
            boxes_to_move = {box}

            if direction == Direction.RIGHT:
                more_boxes = self._get_boxes_to_move(box + Vector(2, 0), Direction.RIGHT)
                if more_boxes is None:
                    return None
                boxes_to_move.update(more_boxes)
            elif direction == Direction.LEFT:
                more_boxes = self._get_boxes_to_move(box + Vector(-1, 0), Direction.LEFT)
                if more_boxes is None:
                    return None
                boxes_to_move.update(more_boxes)
            else:
                more_left_boxes = self._get_boxes_to_move(box + direction.vector, direction)
                if more_left_boxes is None:
                    return None
                boxes_to_move.update(more_left_boxes)

                more_right_boxes = self._get_boxes_to_move(
                    box + Vector(1, 0) + direction.vector, direction
                )
                if more_right_boxes is None:
                    return None
                boxes_to_move.update(more_right_boxes)

            return boxes_to_move

        # Pushing an empty space is allowed but moves no boxes
        return set()

    def move_robot(self, direction: Direction) -> None:
        boxes_to_move = self._get_boxes_to_move(self.robot + direction.vector, direction)
        if boxes_to_move is None:
            return

        self.boxes.difference_update(boxes_to_move)
        self.boxes.update(box + direction.vector for box in boxes_to_move)
        self.robot += direction.vector

    @classmethod
    def from_str(cls, text: str) -> Self:
        # Initialize a room with a sentinel robot vector
        robot_sentinel = Vector(-1, -1)
        room = cls(set(), set(), robot_sentinel)
        for y, line in enumerate(text.split("\n")):
            for x, char in enumerate(line):
                match char:
                    case "#":
                        room.walls.add(Vector(2 * x, y))
                        room.walls.add(Vector(2 * x + 1, y))
                    case "O":
                        room.boxes.add(Vector(2 * x, y))
                    case "@":
                        if room.robot != robot_sentinel:
                            raise ValueError("Multiple robots in room")
                        room.robot = Vector(2 * x, y)
        return room


def part_1(puzzle_input: str) -> str | int:
    room_section, dir_section = puzzle_input.split("\n\n")
    room = SimpleRoom.from_str(room_section)
    directions = [Direction(c) for c in dir_section if not c.isspace()]
    for direction in directions:
        room.move_robot(direction)
    return sum(box.gps_coord for box in room.boxes)


def part_2(puzzle_input: str) -> str | int:
    room_section, dir_section = puzzle_input.split("\n\n")
    room = WideRoom.from_str(room_section)
    directions = [Direction(c) for c in dir_section if not c.isspace()]
    for direction in directions:
        room.move_robot(direction)
    return sum(box.gps_coord for box in room.boxes)
