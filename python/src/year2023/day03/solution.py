from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    row: int
    col: int


@dataclass
class Region:
    start: Location
    digits: list[int]

    def __len__(self) -> int:
        return len(self.digits)

    def __hash__(self) -> int:
        return hash(self.start)

    @property
    def value(self) -> int:
        total = 0
        for digit in self.digits:
            total *= 10
            total += digit
        return total


@dataclass
class Schematic:
    grid: list[str]  # List of rows

    def find_regions(self) -> list[Region]:
        regions: list[Region] = []
        for row in range(len(self.grid)):
            current_region: Region | None = None
            for col, char in enumerate(self.grid[row]):
                if char.isdigit():
                    if current_region is None:
                        # Start a new region
                        current_region = Region(Location(row, col), [int(char)])
                    else:
                        # Add to existing region
                        current_region.digits.append(int(char))
                elif current_region is not None:
                    # Finalize the current region
                    regions.append(current_region)
                    current_region = None

            # At the end of the row, finalize the current region, if any
            if current_region is not None:
                regions.append(current_region)

        return regions

    def is_part_number(self, region: Region) -> bool:
        for row in range(region.start.row - 1, region.start.row + 2):
            for col in range(region.start.col - 1, region.start.col + len(region) + 1):
                if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[row]):
                    char = self.grid[row][col]
                    if char != "." and not char.isdigit():
                        return True
        return False


def part_1(puzzle_input: str) -> str | int:
    schematic = Schematic(puzzle_input.split("\n"))
    total = 0
    for region in schematic.find_regions():
        if schematic.is_part_number(region):
            total += region.value
    return total


def get_adjacent_regions(
    location: Location, location_to_region: dict[Location, Region]
) -> set[Region]:
    regions: set[Region] = set()
    for row_offset in range(-1, 2):
        for col_offset in range(-1, 2):
            if row_offset == 0 and col_offset == 0:
                continue

            neighbor = Location(location.row + row_offset, location.col + col_offset)
            if neighbor not in location_to_region:
                continue

            regions.add(location_to_region[neighbor])

    return regions


def part_2(puzzle_input: str) -> str | int:
    schematic = Schematic(puzzle_input.split("\n"))

    location_to_region: dict[Location, Region] = {}
    for region in schematic.find_regions():
        for char_offset in range(len(region)):
            location = Location(region.start.row, region.start.col + char_offset)
            location_to_region[location] = region

    total = 0
    for row in range(len(schematic.grid)):
        for col, char in enumerate(schematic.grid[row]):
            if char != "*":
                continue

            adjacent_regions = get_adjacent_regions(Location(row, col), location_to_region)
            if len(adjacent_regions) != 2:
                continue

            first, second = adjacent_regions
            total += first.value * second.value

    return total
