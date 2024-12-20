from bisect import bisect_left
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)


def parse_input(puzzle_input: str) -> tuple[list[Vector], Vector]:
    walls = [Vector(*map(int, line.split(","))) for line in puzzle_input.split("\n")]
    max_pos = Vector(max(pos.x for pos in walls), max(pos.y for pos in walls))
    return walls, max_pos


def get_shortest_path(
    wall_list: list[Vector], num_walls_to_use: int, max_pos: Vector
) -> int | None:
    # Queue items are (position, path-length to that position)
    walls = set(wall_list[:num_walls_to_use])
    queue = deque[tuple[Vector, int]]()
    queue.append((Vector(0, 0), 0))
    seen: set[Vector] = {Vector(0, 0)}

    while queue:
        pos_to_expand, dist_so_far = queue.popleft()
        for offset in (Vector(1, 0), Vector(0, 1), Vector(-1, 0), Vector(0, -1)):
            neighbor = pos_to_expand + offset
            if neighbor == max_pos:
                return dist_so_far + 1

            if neighbor in seen or neighbor in walls:
                continue

            if neighbor.x < 0 or neighbor.x > max_pos.x or neighbor.y < 0 or neighbor.y > max_pos.y:
                continue

            seen.add(neighbor)
            queue.append((neighbor, dist_so_far + 1))

    return None


def part_1(puzzle_input: str) -> str | int:
    walls, max_pos = parse_input(puzzle_input)
    num_walls_to_use = 12 if max_pos == Vector(6, 6) else 1024
    shortest_path = get_shortest_path(walls, num_walls_to_use, max_pos)
    if shortest_path is None:
        raise RuntimeError(f"No path using {num_walls_to_use} walls")
    return shortest_path


def part_2(puzzle_input: str) -> str | int:
    walls, max_pos = parse_input(puzzle_input)
    num_walls_to_use = bisect_left(
        range(len(walls)),
        True,
        key=lambda num_to_use: get_shortest_path(walls, num_to_use, max_pos) is None,
    )
    blocking_wall = walls[num_walls_to_use - 1]
    return f"{blocking_wall.x},{blocking_wall.y}"
