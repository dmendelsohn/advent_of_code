from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    row: int
    col: int

    @property
    def neighbors(self) -> list["Location"]:
        """Neighbors in clockwise order"""
        return [
            Location(self.row + row_offset, self.col + col_offset)
            for row_offset, col_offset in ((0, 1), (1, 0), (0, -1), (-1, 0))
        ]


@dataclass
class Region(set[Location]):
    @property
    def area(self) -> int:
        return len(self)

    @property
    def perimeter(self) -> int:
        total = 0
        for loc in self:
            total += sum(1 for neighbor in loc.neighbors if neighbor not in self)
        return total

    @property
    def num_corners(self) -> int:
        total = 0
        for loc in self:
            # Look at each touching pair of neighbors
            # If neither is in the Region, we found a corner
            neighbors = loc.neighbors
            for idx in range(len(neighbors)):
                first, second = neighbors[idx - 1], neighbors[idx]
                diagonal = Location(
                    first.row + second.row - loc.row, first.col + second.col - loc.col
                )
                if first not in self and second not in self:
                    # We found a convex corner
                    total += 1
                elif first in self and second in self and diagonal not in self:
                    # We found a concave corner
                    total += 1
        return total


def explore_region(
    grid: list[list[str]], start: Location, visited: set[Location], region: Region
) -> None:
    region.add(start)
    visited.add(start)
    symbol = grid[start.row][start.col]
    for neighbor in start.neighbors:
        if (
            neighbor not in visited
            and 0 <= neighbor.row < len(grid)
            and 0 <= neighbor.col < len(grid[0])
            and grid[neighbor.row][neighbor.col] == symbol
        ):
            explore_region(grid, neighbor, visited, region)


def get_regions(grid: list[list[str]]) -> list[Region]:
    regions: list[Region] = []
    visited: set[Location] = set()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            start = Location(row, col)
            if start not in visited:
                region = Region()
                explore_region(grid, start, visited, region)
                regions.append(region)
    return regions


def part_1(puzzle_input: str) -> str | int:
    grid = [list(line) for line in puzzle_input.split("\n")]
    regions = get_regions(grid)
    return sum(region.area * region.perimeter for region in regions)


def part_2(puzzle_input: str) -> str | int:
    grid = [list(line) for line in puzzle_input.split("\n")]
    regions = get_regions(grid)
    return sum(region.area * region.num_corners for region in regions)
