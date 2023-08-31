from collections import deque
from itertools import combinations
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int
    z: int

    @property
    def neighbors(self) -> set["Point"]:
        neighbors = set()
        for x_offset in (-1, 1):
            neighbors.add(Point(self.x + x_offset, self.y, self.z))
        for y_offset in (-1, 1):
            neighbors.add(Point(self.x, self.y + y_offset, self.z))
        for z_offset in (-1, 1):
            neighbors.add(Point(self.x, self.y, self.z + z_offset))
        return neighbors


def parse_input(puzzle_input: str) -> set[Point]:
    points = set()
    for line in puzzle_input.split("\n"):
        point = Point(*(int(num) for num in line.split(",")))
        points.add(point)
    return points


def is_adjacent(first: Point, second: Point) -> bool:
    return abs(first.x - second.x) + abs(first.y - second.y) + abs(first.z - second.z) == 1


def part_1(puzzle_input: str) -> str | int:
    points = parse_input(puzzle_input)
    num_touching = 0
    for first, second in combinations(points, 2):
        if is_adjacent(first, second):
            num_touching += 1

    return 6 * len(points) - 2 * num_touching


def part_2(puzzle_input: str) -> str | int:
    occupied = parse_input(puzzle_input)

    # Establish a bounding box (with a buffer around the periphery)
    min_x, max_x = min(p.x for p in occupied) - 1, max(p.x for p in occupied) + 1
    min_y, max_y = min(p.y for p in occupied) - 1, max(p.y for p in occupied) + 1
    min_z, max_z = min(p.z for p in occupied) - 1, max(p.z for p in occupied) + 1

    # BFS to find all empty spaces connected to the outside
    start = Point(min_x, min_y, min_z)
    outside = {start}
    queue = deque([start])
    while queue:
        point = queue.popleft()
        for neighbor in point.neighbors:
            if neighbor in outside:
                # Already seen
                continue
            if neighbor in occupied:
                # Not empty
                continue

            # Check boundary conditions to not limit search to bounding box
            if neighbor.x < min_x or neighbor.x > max_x:
                continue
            if neighbor.y < min_y or neighbor.y > max_y:
                continue
            if neighbor.z < min_z or neighbor.z > max_z:
                continue

            outside.add(neighbor)
            queue.append(neighbor)

    # Now for all the empty spaces, count occupied neighbors
    num_faces = 0
    for outside_point in outside:
        for neighbor in outside_point.neighbors:
            if neighbor in occupied:
                num_faces += 1
    return num_faces
