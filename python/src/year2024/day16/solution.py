from dataclasses import dataclass
from functools import total_ordering
from heapq import heapify, heappop, heappush


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    @property
    def rot_90(self) -> "Vector":
        """Rotate 90 degrees clockwise"""
        return Vector(-self.y, self.x)


@dataclass
class Maze:
    grid: list[list[bool]]  # True when there is a wall, False otherwise
    start: Vector
    end: Vector

    def __str__(self) -> str:
        lines: list[str] = []
        for y, row in enumerate(self.grid):
            line: list[str] = []
            for x, is_wall in enumerate(row):
                if is_wall:
                    line.append("#")
                elif Vector(x, y) == self.start:
                    line.append("S")
                elif Vector(x, y) == self.end:
                    line.append("E")
                else:
                    line.append(".")
            lines.append("".join(line))
        return "\n".join(lines)

    def get_neighbors(self, position: Vector, heading: Vector) -> set[tuple[Vector, Vector, int]]:
        """
        Calculate possible transitions from the given position and heading.
        Returns a set of (position, heading, cost) tuples
        """
        # 90 degree turns in either direction
        neighbors: set[tuple[Vector, Vector, int]] = {
            (position, heading.rot_90, 1000),
            (position, heading.rot_90.rot_90.rot_90, 1000),
        }

        # we may also be able to move forward
        forward = position + heading
        if not self.grid[forward.y][forward.x]:
            neighbors.add((forward, heading, 1))

        return neighbors

    def get_min_cost_and_waypoints(self) -> tuple[int, frozenset[Vector]]:
        """
        Get weight of shortest path from the start to the end using Dijkstra.
        Also return all positions on any shortest path from the start to the end.
        """

        @total_ordering
        @dataclass(frozen=True)
        class HeapItem:
            # The current "node" is specified by position and heading
            position: Vector
            heading: Vector
            cost_so_far: int  # Least cost to get to this node from the start
            waypoints: frozenset[Vector]  # Positions along any shortest path to this node

            def __lt__(self, other: "HeapItem") -> bool:
                return self.cost_so_far < other.cost_so_far

        # Initialize min heap of nodes and total cost to get there
        unexpanded_nodes: list[HeapItem] = [
            HeapItem(self.start, Vector(1, 0), 0, frozenset({self.start}))
        ]

        # Track (position, vector) states we've expanded already so we don't retrace our steps
        expanded_nodes: set[tuple[Vector, Vector]] = set()

        while unexpanded_nodes:
            expanded_heap_item = heappop(unexpanded_nodes)
            if expanded_heap_item.position == self.end:
                # We found the shortest paths to the end!
                return expanded_heap_item.cost_so_far, expanded_heap_item.waypoints

            expanded_nodes.add((expanded_heap_item.position, expanded_heap_item.heading))
            for neighbor_pos, neighbor_heading, weight in self.get_neighbors(
                expanded_heap_item.position, expanded_heap_item.heading
            ):
                if (neighbor_pos, neighbor_heading) in expanded_nodes:
                    continue

                if (neighbor_pos, neighbor_heading.rot_90.rot_90) in expanded_nodes:
                    # No reason to retrace our steps
                    continue

                # Check if the neighbor is already in the unexpanded nodes heap
                neighbor_idx_in_heap: int | None = None
                for idx, _heap_item in enumerate(unexpanded_nodes):
                    if (
                        neighbor_pos == _heap_item.position
                        and neighbor_heading == _heap_item.heading
                    ):
                        neighbor_idx_in_heap = idx
                        break

                neighbor_cost = expanded_heap_item.cost_so_far + weight
                if neighbor_idx_in_heap is None:
                    # Neighbor not in unexpanded nodes heap, so let's add it
                    new_heap_item = HeapItem(
                        neighbor_pos,
                        neighbor_heading,
                        neighbor_cost,
                        expanded_heap_item.waypoints | {neighbor_pos},
                    )
                    heappush(unexpanded_nodes, new_heap_item)
                else:
                    existing_heap_item = unexpanded_nodes[neighbor_idx_in_heap]
                    if neighbor_cost <= existing_heap_item.cost_so_far:
                        # Remove the existing element in the heap...
                        unexpanded_nodes.pop(neighbor_idx_in_heap)
                        heapify(unexpanded_nodes)

                        # ... and replace it with a new element
                        waypoints = expanded_heap_item.waypoints | {neighbor_pos}
                        if neighbor_cost == existing_heap_item.cost_so_far:
                            # All existing waypoints are still waypoints
                            waypoints |= existing_heap_item.waypoints

                        new_heap_item = HeapItem(
                            neighbor_pos, neighbor_heading, neighbor_cost, waypoints
                        )
                        heappush(unexpanded_nodes, new_heap_item)

        raise ValueError("Could not find a path to the end position")


def parse_input(puzzle_input: str) -> Maze:
    grid: list[list[bool]] = []
    start: Vector | None = None
    end: Vector | None = None
    for y, line in enumerate(puzzle_input.split("\n")):
        row = []
        for x, char in enumerate(line):
            if char == "S":
                start = Vector(x, y)
            elif char == "E":
                end = Vector(x, y)

            row.append(char == "#")
        grid.append(row)

    assert start is not None
    assert end is not None
    return Maze(grid, start, end)


def part_1(puzzle_input: str) -> str | int:
    maze = parse_input(puzzle_input)
    return maze.get_min_cost_and_waypoints()[0]


def part_2(puzzle_input: str) -> str | int:
    maze = parse_input(puzzle_input)
    return len(maze.get_min_cost_and_waypoints()[1])
