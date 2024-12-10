from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    row: int
    col: int


class Grid(list[list[int]]):
    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self)

    def get_height(self, location: Location) -> int | None:
        if 0 <= location.row < self.num_rows:
            if 0 <= location.col < self.num_cols:
                return self[location.row][location.col]
        return None

    @classmethod
    def from_input(cls, puzzle_input: str) -> "Grid":
        return cls([[int(char) for char in line] for line in puzzle_input.split("\n")])

    @property
    def num_rows(self):
        return len(self)

    @property
    def num_cols(self):
        return len(self[0])

    def get_trails(self, start_loc: Location) -> list[list[Location]]:
        """
        Return a list of valid trails from start_loc
        Each trail is a list of location starting from the end of the trail
        """
        if (start_height := self[start_loc.row][start_loc.col]) == 9:
            return [[start_loc]]

        trails: list[list[Location]] = []
        for row_offset, col_offset in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            neighbor = Location(start_loc.row + row_offset, start_loc.col + col_offset)
            if self.get_height(neighbor) == start_height + 1:
                for subtrail in self.get_trails(neighbor):
                    subtrail.append(start_loc)
                    trails.append(subtrail)
        return trails

    def get_trailheads(self) -> set[Location]:
        zeros: set[Location] = set()
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self[row][col] == 0:
                    zeros.add(Location(row, col))
        return zeros


def part_1(puzzle_input: str) -> str | int:
    grid = Grid.from_input(puzzle_input)
    total_score = 0
    for start in grid.get_trailheads():
        trails = grid.get_trails(start)
        endpoints = {trail[0] for trail in trails}
        total_score += len(endpoints)
    return total_score


def part_2(puzzle_input: str) -> str | int:
    grid = Grid.from_input(puzzle_input)
    total_score = 0
    for start in grid.get_trailheads():
        trails = grid.get_trails(start)
        total_score += len(trails)
    return total_score
