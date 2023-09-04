from enum import Enum
from typing import NamedTuple


class Location(NamedTuple):
    row: int
    col: int


def parse_locations(text: str) -> list[Location]:
    locations = []
    for coords in text.split(" -> "):
        col, row = map(int, coords.split(","))
        locations.append(Location(row, col))
    return locations


class Object(Enum):
    SAND = "o"
    WALL = "#"


class Cave:
    def __init__(self, puzzle_input: str, *, is_solid_floor: bool):
        self._start = Location(0, 500)
        self._contents: dict[Location, Object] = {}
        for line in puzzle_input.split("\n"):
            locations = parse_locations(line)
            for i in range(len(locations) - 1):
                self._add_wall(locations[i], locations[i + 1])

        # We use an infinite floor either way, and conditionally choose whether
        # Sand can actually rest there depending on self._is_solid_flor
        self._floor_row = max(loc.row for loc in self._contents) + 2
        self._is_solid_floor = is_solid_floor

    def _add_wall(self, start: Location, end: Location) -> None:
        if start.row == end.row:
            for col in range(min(start.col, end.col), max(start.col, end.col) + 1):
                self._contents[Location(start.row, col)] = Object.WALL
        elif start.col == end.col:
            for row in range(min(start.row, end.row), max(start.row, end.row) + 1):
                self._contents[Location(row, start.col)] = Object.WALL
        else:
            raise ValueError(f"Cannot build diagonal wall from {start} to {end}")

    def drop_sand(self) -> bool:
        """Place a new piece of sand if possible (return whether it was possible)"""
        # Cannot even start movement if the start location is occupied
        if self._start in self._contents:
            return False

        # Apply movement rules until we cannot move anymore
        pos = self._start
        while True:
            next_pos = pos
            for col_offset in (0, -1, 1):
                neighbor = Location(pos.row + 1, pos.col + col_offset)
                if neighbor not in self._contents and neighbor.row != self._floor_row:
                    next_pos = neighbor
                    break

            if next_pos == pos:
                # No more movement, break
                break
            else:
                pos = next_pos

        if not self._is_solid_floor and pos.row + 1 == self._floor_row:
            # Cannot place sand because floor is not solid, it should fall through
            return False
        else:
            self._contents[pos] = Object.SAND
            return True

    def fill(self) -> int:
        num_sand = 0
        while self.drop_sand():
            num_sand += 1
        return num_sand


def part_1(puzzle_input: str) -> str | int:
    return Cave(puzzle_input, is_solid_floor=False).fill()


def part_2(puzzle_input: str) -> str | int:
    return Cave(puzzle_input, is_solid_floor=True).fill()
