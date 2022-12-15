from collections import defaultdict
from pathlib import Path
import re
from typing import NamedTuple, Set

INPUT_PATH = Path(__file__).parent / "input.txt"


class Point(NamedTuple):
    x: int
    y: int


class Segment(NamedTuple):
    x1: int
    y1: int
    x2: int
    y2: int


def is_45_degrees(segment: Segment) -> bool:
    return abs(segment.x2 - segment.x1) == abs(segment.y2 - segment.y1)


def segment_points(segment: Segment, include_diagonals: bool) -> Set[Point]:
    if segment.x1 == segment.x2:
        min_y = min(segment.y1, segment.y2)
        max_y = max(segment.y1, segment.y2)
        return {Point(segment.x1, y) for y in range(min_y, max_y + 1)}
    elif segment.y1 == segment.y2:
        min_x = min(segment.x1, segment.x2)
        max_x = max(segment.x1, segment.x2)
        return {Point(x, segment.y1) for x in range(min_x, max_x + 1)}
    elif include_diagonals and is_45_degrees(segment):
        points = set()
        x = segment.x1
        xstep = 1 if segment.x2 > segment.x1 else -1
        y = segment.y1
        ystep = 1 if segment.y2 > segment.y1 else -1
        while x != segment.x2:
            points.add(Point(x, y))
            x += xstep
            y += ystep
        points.add(Point(x, y))
        return points
    else:
        return set()


def parse_line(line: str) -> Segment:
    # e.g. "504,971 -> 989,971"
    pattern = "([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)"
    match = re.match(pattern, line)
    if not match:
        raise ValueError(f"Could not parse line: {line}")
    return Segment(*(int(elt) for elt in match.groups()))


def parse_input() -> Set[Segment]:
    return {parse_line(line) for line in open(INPUT_PATH).read().strip().split("\n")}


def part_1() -> str:
    segments = parse_input()
    point_counts = defaultdict(int)
    for segment in segments:
        for point in segment_points(segment, include_diagonals=False):
            point_counts[point] += 1
    dangerous_points = {point for point, count in point_counts.items() if count >= 2}
    print(f"Dangerous points: {dangerous_points}")
    print(f"Num dangerous points: {len(dangerous_points)}")
    return f"{len(dangerous_points)}"


def part_2() -> str:
    segments = parse_input()
    point_counts = defaultdict(int)
    for segment in segments:
        for point in segment_points(segment, include_diagonals=True):
            point_counts[point] += 1
    dangerous_points = {point for point, count in point_counts.items() if count >= 2}
    print(f"Dangerous points: {dangerous_points}")
    print(f"Num dangerous points: {len(dangerous_points)}")
    return f"{len(dangerous_points)}"
