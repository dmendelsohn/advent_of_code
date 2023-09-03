from collections import defaultdict
from enum import Enum
from typing import NamedTuple


class Direction(Enum):
    NORTHWEST = (-1, -1)
    NORTH = (-1, 0)
    NORTHEAST = (-1, 1)
    EAST = (0, 1)
    SOUTHEAST = (1, 1)
    SOUTH = (1, 0)
    SOUTHWEST = (1, -1)
    WEST = (0, -1)


class Point(NamedTuple):
    row: int
    col: int


Elves = set[Point]


def parse_input(text: str) -> Elves:
    output = set()
    for row, line in enumerate(text.split("\n")):
        for col, char in enumerate(line):
            if char == "#":
                output.add(Point(row, col))
    return output


def get_occupied_directions(elves: Elves, point: Point) -> set[Direction]:
    return {
        direction
        for direction in Direction
        if Point(point.row + direction.value[0], point.col + direction.value[1]) in elves
    }


def get_proposed_move(elves: Elves, point: Point, directions: list[Direction]) -> Point:
    occupied_dirs = get_occupied_directions(elves, point)
    if not occupied_dirs:
        # Space in all directions, no need to move
        return point

    for direction in directions:
        # Check spot to move to
        if direction in occupied_dirs:
            continue

        # Check diagonals too
        if direction == Direction.NORTH:
            if Direction.NORTHWEST in occupied_dirs or Direction.NORTHEAST in occupied_dirs:
                continue
        elif direction == Direction.SOUTH:
            if Direction.SOUTHWEST in occupied_dirs or Direction.SOUTHEAST in occupied_dirs:
                continue
        elif direction == Direction.WEST:
            if Direction.NORTHWEST in occupied_dirs or Direction.SOUTHWEST in occupied_dirs:
                continue
        elif direction == Direction.EAST:
            if Direction.NORTHEAST in occupied_dirs or Direction.SOUTHEAST in occupied_dirs:
                continue

        # Found the direction to move in
        return Point(point.row + direction.value[0], point.col + direction.value[1])

    # Can't move anywhere, stay still
    return point


def full_step(elves: Elves, directions: list[Direction]) -> Elves:
    # First calculate the proposals
    proposed_targets = defaultdict(set)  # Maps targets to elves proposing move to there
    for elf in elves:
        target = get_proposed_move(elves, elf, directions)
        proposed_targets[target].add(elf)

    # Then resolve the proposals
    output = set()
    for target, elves_targeting in proposed_targets.items():
        if len(elves_targeting) == 1:
            # No conflict, elf can move to this target
            output.add(target)
        elif len(elves_targeting) > 1:
            # Conflict, elves should stay where they are
            output.update(elves_targeting)
    return output


def get_space_in_bounding_box(elves: Elves) -> int:
    height = max(elf.row for elf in elves) - min(elf.row for elf in elves) + 1
    width = max(elf.col for elf in elves) - min(elf.col for elf in elves) + 1
    return height * width - len(elves)


def part_1(puzzle_input: str) -> str | int:
    elves = parse_input(puzzle_input)
    directions = [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]
    for _ in range(10):
        elves = full_step(elves, directions)
        directions.append(directions.pop(0))
    return get_space_in_bounding_box(elves)


def part_2(puzzle_input: str) -> str | int:
    elves = parse_input(puzzle_input)
    directions = [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]
    num_steps = 0
    while True:
        new_elves = full_step(elves.copy(), directions)
        directions.append(directions.pop(0))
        num_steps += 1
        if elves == new_elves:
            return num_steps
        else:
            elves = new_elves
