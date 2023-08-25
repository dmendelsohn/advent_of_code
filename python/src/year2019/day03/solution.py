from enum import Enum
from functools import total_ordering
from typing import NamedTuple, Optional


class Direction(Enum):
    UP = "U"
    DOWN = "D"
    RIGHT = "R"
    LEFT = "L"


class Command(NamedTuple):
    direction: Direction
    distance: int

    @classmethod
    def parse(cls, text: str) -> "Command":
        return cls(direction=Direction(text[0]), distance=int(text[1:]))

    @property
    def offset(self) -> tuple[int, int]:
        # Returns (lat, lon) of the offset
        match self.direction:
            case Direction.UP:
                return self.distance, 0
            case Direction.DOWN:
                return -self.distance, 0
            case Direction.RIGHT:
                return 0, self.distance
            case Direction.LEFT:
                return 0, -self.distance
            case _:
                raise ValueError(f"Unrecognized direction {self.direction}")


def parse_line(text: str) -> list[Command]:
    return [Command.parse(com) for com in text.split(",")]


def parse_input(text: str) -> tuple[list[Command], list[Command]]:
    lines = text.split("\n")
    if len(lines) != 2:
        raise ValueError(f"Expected two lines, not {len(lines)}")
    return parse_line(lines[0]), parse_line(lines[1])


@total_ordering
class Point(NamedTuple):
    lat: int
    lon: int

    @property
    def magnitude(self) -> int:
        return abs(self.lat) + abs(self.lon)


class Segment(NamedTuple):
    start: Point
    end: Point

    @property
    def is_horizontal(self) -> bool:
        return self.start.lat == self.end.lat

    @property
    def is_vertical(self) -> bool:
        return self.start.lon == self.end.lon

    @property
    def normalized(self) -> "Segment":
        return Segment(min(self.start, self.end), max(self.start, self.end))

    @property
    def length(self) -> int:
        # Return the taxicab length of the segment
        return abs(self.start.lon - self.end.lon) + abs(self.start.lat - self.end.lat)


def calculate_segments(commands: list[Command]) -> list[Segment]:
    segments = []
    current = Point(0, 0)
    for command in commands:
        next_point = Point(current.lat + command.offset[0], current.lon + command.offset[1])
        segments.append(Segment(current, next_point))
        current = next_point
    return segments


def get_intersection(first: Segment, second: Segment) -> Optional[Point]:
    # If multiple intersections (e.g. segments are overlapping), return closest to origin
    # If no intersections, return None
    first = first.normalized
    second = second.normalized

    if first.is_horizontal and second.is_horizontal:
        if first.start.lat != second.start.lat:
            return None

        highest_min = max(first.start.lon, second.start.lon)
        lowest_max = min(first.end.lon, second.end.lon)
        if highest_min > lowest_max:
            # No overlap
            return None

        # In our puzzle data, this doesn't actually happen except at the origin
        if highest_min * lowest_max <= 0:
            # Crosses axis
            return Point(first.start.lat, 0)
        elif highest_min > 0:
            # Entirely right of axis
            return Point(first.start.lat, highest_min)
        else:
            # Entirely left of axis
            return Point(first.start.lat, lowest_max)

    elif first.is_vertical and second.is_vertical:
        if first.start.lon != second.start.lon:
            return None

        highest_min = max(first.start.lat, second.start.lat)
        lowest_max = min(first.end.lat, second.end.lat)
        if highest_min > lowest_max:
            # No overlap
            return None

        # In our puzzle data, this doesn't actually happen except at the origin
        if highest_min * lowest_max <= 0:
            # Crosses axis
            return Point(0, first.start.lon)
        elif highest_min > 0:
            # Entirely above axis
            return Point(highest_min, first.start.lon)
        else:
            # Entirely below axis
            return Point(lowest_max, first.start.lon)

    # We can assume we have one vertical and one horizontal
    # Now check if they cross
    vertical = next(seg for seg in [first, second] if seg.is_vertical)
    horizontal = next(seg for seg in [first, second] if seg.is_horizontal)
    if horizontal.start.lon <= vertical.start.lon <= horizontal.end.lon:
        if vertical.start.lat <= horizontal.start.lat <= vertical.end.lat:
            return Point(horizontal.start.lat, vertical.start.lon)

    return None


def part_1(puzzle_input: str) -> str | int:
    commands0, commands1 = parse_input(puzzle_input)
    segments0, segments1 = calculate_segments(commands0), calculate_segments(commands1)
    min_intersection: Optional[Point] = None
    for seg0 in segments0:
        for seg1 in segments1:
            intersection = get_intersection(seg0, seg1)
            if intersection and intersection != Point(0, 0):
                if min_intersection is None or min_intersection.magnitude > intersection.magnitude:
                    min_intersection = intersection

    if min_intersection is None:
        raise ValueError("Could not find an intersection")

    return abs(min_intersection.lat) + abs(min_intersection.lon)


class Intersection(NamedTuple):
    point: Point
    delay: int  # Total delay of two signals to reach this intersection


def part_2(puzzle_input: str) -> str | int:
    commands0, commands1 = parse_input(puzzle_input)
    segments0, segments1 = calculate_segments(commands0), calculate_segments(commands1)
    min_delay: Optional[int] = None
    delay0 = 0
    for seg0 in segments0:
        delay1 = 0
        for seg1 in segments1:
            intersection = get_intersection(seg0, seg1)
            if intersection and intersection != Point(0, 0):
                total_delay = (
                    delay0
                    + delay1
                    + Segment(seg0.start, intersection).length
                    + Segment(seg1.start, intersection).length
                )
                if min_delay is None or min_delay > total_delay:
                    min_delay = total_delay

            delay1 += seg1.length
        delay0 += seg0.length

    if min_delay is None:
        raise ValueError("Could not find an intersection")

    return min_delay
