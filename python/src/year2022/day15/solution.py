import re
from typing import Iterable, NamedTuple, Optional


class Range(NamedTuple):
    """Represents an inclusive integer range"""

    low: int
    high: int

    @property
    def width(self):
        return self.high - self.low + 1

    def is_touching(self, other: "Range") -> bool:
        # "gap" between two ranges is max(lows) - min(highs)
        return max(self.low, other.low) - min(self.high, other.high) <= 1

    def merge(self, other: "Range") -> "Range":
        if self.is_touching(other):
            return Range(low=min(self.low, other.low), high=max(self.high, other.high))
        else:
            raise ValueError("Cannot merge ranges that have a gap")


class Point(NamedTuple):
    x: int
    y: int

    def distance_from(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class Sensor(NamedTuple):
    location: Point
    nearest_beacon: Point

    def get_xrange_within_beacon_dist(self, y: int) -> Optional[Range]:
        x_dist = self.location.distance_from(self.nearest_beacon) - abs(self.location.y - y)
        if x_dist < 0:
            return None
        return Range(self.location.x - x_dist, self.location.x + x_dist)


def merge_ranges(ranges: Iterable[Range]) -> list[Range]:
    """Combine overlapping and touches ranges and return result in sorted order"""
    ranges = sorted(ranges)
    output: list[Range] = []
    for new_range in sorted(ranges):
        if output and output[-1].is_touching(new_range):
            last_range = output.pop()
            output.append(new_range.merge(last_range))
        else:
            output.append(new_range)
    return output


def get_xranges_within_beacon_dist(sensors: set[Sensor], y: int) -> list[Range]:
    """
    Return the list of x-ranges that cannot have they mystery beacon.
    Output ranges will be sorted, non-overlapping, and non-adjacent.
    """
    xranges = (sensor.get_xrange_within_beacon_dist(y) for sensor in sensors)
    return merge_ranges(r for r in xranges if r)


def parse_input(text: str) -> set[Sensor]:
    sensors = set()
    pattern = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    for line in text.split("\n"):
        match = re.match(pattern, line)
        if not match:
            raise ValueError(f"Could not parse {line=}")

        sensor_x, sensor_y, beacon_x, beacon_y = map(int, match.groups())
        sensors.add(
            Sensor(location=Point(sensor_x, sensor_y), nearest_beacon=Point(beacon_x, beacon_y))
        )
    return sensors


def part_1(puzzle_input: str) -> str | int:
    sensors = parse_input(puzzle_input)
    y = 10 if len(sensors) == 14 else 2000000  # Different y values for example and real cases
    xranges = get_xranges_within_beacon_dist(sensors, y)

    # Count the total size of all the ranges, subtracting out number of beacons in some range
    total = sum(r.width for r in xranges)

    beacons_to_discount = set()
    for sensor in sensors:
        if sensor.nearest_beacon.y != y:
            continue
        if any(r.low <= sensor.nearest_beacon.x <= r.high for r in xranges):
            beacons_to_discount.add(sensor.nearest_beacon)

    total -= len(beacons_to_discount)
    return total


class Segment(NamedTuple):
    """Represents a diagonal (slope = 1 or -1) segment"""

    start: Point  # Leftmost (min x) point
    length: int  # Length (start.x + length) is x-coord last point on the segment)
    is_positive_slope: bool  # Indicates if slope is 1 or -1

    def intersect(self, other: "Segment") -> Optional[Point]:
        """
        For segments of differing slopes, calculate their intersection point (if any)
        We ignore non-integer intersection points
        """
        if self.is_positive_slope == other.is_positive_slope:
            return None

        # Find intersection of the two lines
        # y = x + b and y = -x + c intersect at x = (c - b) / 2
        positive = next(seg for seg in (self, other) if seg.is_positive_slope)
        positive_y_intercept = positive.start.y - positive.start.x

        negative = next(seg for seg in (self, other) if not seg.is_positive_slope)
        negative_y_intercept = negative.start.y + negative.start.x

        y_intercept_diff = negative_y_intercept - positive_y_intercept
        if y_intercept_diff % 2 == 1:
            return None

        x_intersection = y_intercept_diff // 2

        if (
            0 <= x_intersection - positive.start.x <= positive.length
            and 0 <= x_intersection - negative.start.x <= negative.length
        ):
            y_intersection = positive.start.y + (x_intersection - positive.start.x)
            return Point(x_intersection, y_intersection)

        return None


def can_have_mystery_beacon(point: Point, sensors: set[Sensor], bound: int) -> bool:
    if point.x < 0 or point.x > bound or point.y < 0 or point.y > bound:
        return False

    for sensor in sensors:
        if sensor.location.distance_from(point) <= sensor.location.distance_from(
            sensor.nearest_beacon
        ):
            return False
    return True


def tuning_frequency(point: Point) -> int:
    return 4000000 * point.x + point.y


def part_2(puzzle_input: str) -> str | int:
    # This part takes a minute to run, but I can't think of an asymptotically faster way to do it
    sensors = parse_input(puzzle_input)
    bound = 20 if len(sensors) == 14 else 4000000  # Different bounds for example and real cases

    segments = []
    for sensor in sensors:
        center = sensor.location
        radius = sensor.location.distance_from(sensor.nearest_beacon)
        segments.append(
            Segment(start=Point(center.x - radius, center.y), length=radius, is_positive_slope=True)
        )
        segments.append(
            Segment(
                start=Point(center.x - radius, center.y), length=radius, is_positive_slope=False
            )
        )
        segments.append(
            Segment(start=Point(center.x, center.y - radius), length=radius, is_positive_slope=True)
        )
        segments.append(
            Segment(
                start=Point(center.x, center.y + radius), length=radius, is_positive_slope=False
            )
        )

    intersections = set()
    for i in range(len(segments)):
        for j in range(i + 1, len(segments)):
            intersection = segments[i].intersect(segments[j])
            if intersection:
                intersections.add(intersection)

    uncovered_points = set()
    for intersection in intersections:
        for delta_x, delta_y in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            neighbor = Point(intersection.x + delta_x, intersection.y + delta_y)
            if can_have_mystery_beacon(neighbor, sensors, bound):
                uncovered_points.add(neighbor)

    if len(uncovered_points) != 1:
        raise RuntimeError(f"Did not get exactly one candidate point: {uncovered_points}")

    return tuning_frequency(uncovered_points.pop())
