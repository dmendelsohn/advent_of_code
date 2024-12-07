from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"

    def turn_right(self) -> "Direction":
        dirs = (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT)
        idx = dirs.index(self)
        next_idx = (idx + 1) % len(dirs)
        return dirs[next_idx]


@dataclass(frozen=True)
class Location:
    row: int
    col: int

    def step(self, direction: Direction) -> "Location":
        match direction:
            case Direction.UP:
                return Location(self.row - 1, self.col)
            case Direction.DOWN:
                return Location(self.row + 1, self.col)
            case Direction.LEFT:
                return Location(self.row, self.col - 1)
            case Direction.RIGHT:
                return Location(self.row, self.col + 1)


@dataclass(frozen=True)
class GuardState:
    location: Location
    direction: Direction


@dataclass
class Area:
    num_rows: int
    num_cols: int
    obstacles: set[Location]

    def is_in_bounds(self, location) -> bool:
        return 0 <= location.row < self.num_rows and 0 <= location.col < self.num_cols

    def next_guard_state(self, guard: GuardState) -> GuardState:
        next_guard_direction = guard.direction
        while (next_guard_location := guard.location.step(next_guard_direction)) in self.obstacles:
            next_guard_direction = next_guard_direction.turn_right()
        return GuardState(next_guard_location, next_guard_direction)

    def to_str(self, guard: GuardState) -> str:
        row_strs: list[str] = []
        for row_idx in range(self.num_rows):
            row: list[str] = []
            for col_idx in range(self.num_cols):
                location = Location(row_idx, col_idx)
                if location in self.obstacles:
                    row.append("#")
                elif location == guard.location:
                    row.append(guard.direction.value)
                else:
                    row.append(".")

            row_strs.append("".join(row))
        return "\n".join(row_strs)


def parse_input(input: str) -> tuple[Area, GuardState]:
    obstacles: set[Location] = set()
    guard: GuardState | None = None
    rows = input.split("\n")
    for row_idx, row in enumerate(rows):
        for col_idx, symbol in enumerate(row):
            if symbol == "#":
                obstacles.add(Location(row_idx, col_idx))
            elif symbol == ".":
                pass
            else:
                guard = GuardState(Location(row_idx, col_idx), Direction(symbol))

    assert guard is not None
    area = Area(len(rows), len(rows[0]), obstacles)
    return area, guard


def part_1(puzzle_input: str) -> str | int:
    area, guard = parse_input(puzzle_input)
    visited: set[Location] = set()
    while area.is_in_bounds(guard.location):
        visited.add(guard.location)
        guard = area.next_guard_state(guard)
    return len(visited)


def has_loop(area: Area, guard: GuardState) -> bool:
    seen: set[GuardState] = set()
    while area.is_in_bounds(guard.location):
        if guard in seen:
            return True
        seen.add(guard)
        guard = area.next_guard_state(guard)
    return False


def part_2(puzzle_input: str) -> str | int:
    area, guard = parse_input(puzzle_input)
    looping_locations: set[Location] = set()
    visited: set[Location] = set()
    while area.is_in_bounds(guard.location):
        visited.add(guard.location)
        next_guard = area.next_guard_state(guard)
        assert next_guard.location not in area.obstacles

        # Check if putting obstacle in this locatio would result in a loop
        if next_guard.location not in visited:
            area.obstacles.add(next_guard.location)
            if has_loop(area, guard):
                looping_locations.add(next_guard.location)
            area.obstacles.remove(next_guard.location)

        guard = next_guard

    return len(looping_locations)
