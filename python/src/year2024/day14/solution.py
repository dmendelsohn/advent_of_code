import operator
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from typing import DefaultDict


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int) -> "Vector":
        return Vector(self.x * other, self.y * other)

    def __mod__(self, other: "Vector") -> "Vector":
        return Vector(self.x % other.x, self.y % other.y)


@dataclass
class Robot:
    position: Vector
    velocity: Vector

    @classmethod
    def from_line(cls, line: str) -> "Robot":
        if (match := re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)) is None:
            raise ValueError(f"Could not parse line: {line}")
        px, py, vx, vy = map(int, match.groups())
        return cls(Vector(px, py), Vector(vx, vy))

    def move(self, boundary: Vector, num_seconds: int) -> None:
        self.position = (self.position + self.velocity * num_seconds) % boundary


def part_1(puzzle_input: str) -> str | int:
    robots = [Robot.from_line(line) for line in puzzle_input.split("\n")]
    boundary = Vector(1 + max(r.position.x for r in robots), 1 + max(r.position.y for r in robots))
    middle = Vector(boundary.x // 2, boundary.y // 2)
    quadrant_counts: DefaultDict[tuple[bool, bool], int] = defaultdict(int)
    for robot in robots:
        robot.move(boundary, 100)

        # Determine the quadrant the robot ends up in
        if robot.position.x == middle.x or robot.position.y == middle.y:
            continue

        x_quadrant = robot.position.x > middle.x
        y_quadrant = robot.position.y > middle.y
        quadrant_counts[(x_quadrant, y_quadrant)] += 1

    return reduce(operator.mul, quadrant_counts.values(), 1)


def format_robots(robots: list[Robot], boundary: Vector) -> str:
    occupied = {r.position for r in robots}
    lines = []
    for y in range(boundary.y):
        line = []
        for x in range(boundary.x):
            line.append("1" if Vector(x, y) in occupied else " ")
        lines.append("".join(line))
    return "\n".join(lines)


def part_2(puzzle_input: str) -> str | int:
    robots = [Robot.from_line(line) for line in puzzle_input.split("\n")]
    boundary = Vector(1 + max(r.position.x for r in robots), 1 + max(r.position.y for r in robots))

    # Stop condition is when no robots overlap
    num_steps = 0
    while len({r.position for r in robots}) < len(robots):
        for robot in robots:
            robot.move(boundary, 1)
        num_steps += 1

    # Uncomment to see the tree
    # print(format_robots(robots, boundary))
    return num_steps
