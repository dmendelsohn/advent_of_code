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


def complement_ranges(ranges: list[Range], min_val: int, max_val: int) -> list[Range]:
    """Given a sorted list of non-touching ranges, return the complement"""
    if not ranges:
        return [Range(min_val, max_val)]

    complements = []
    if ranges[0].low > min_val:
        complements.append(Range(min_val, ranges[0].low - 1))

    # Add a complement in each gap
    for idx in range(len(ranges) - 1):
        gap = Range(ranges[idx].high + 1, ranges[idx + 1].low - 1)

        bounded_gap = Range(max(min_val, gap.low), min(max_val, gap.high))
        if bounded_gap.low <= bounded_gap.high:
            complements.append(bounded_gap)

    if ranges[-1].high < max_val:
        complements.append(Range(ranges[-1].high + 1, max_val))

    return complements


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


def part_2(puzzle_input: str) -> str | int:
    # This part takes a minute to run, but I can't think of an asymptotically faster way to do it
    sensors = parse_input(puzzle_input)
    bound = 20 if len(sensors) == 14 else 4000000  # Different bounds for example and real cases

    for y in range(bound + 1):
        xranges = get_xranges_within_beacon_dist(sensors, y)
        uncovered_ranges = complement_ranges(xranges, 0, bound)
        if not uncovered_ranges:
            # Completely covered y-coord, move on to the next one
            continue

        if len(uncovered_ranges) > 1 or uncovered_ranges[0].width > 1:
            raise ValueError(f"Got multiple possible locations at {y=}. Ranges: {uncovered_ranges}")

        return uncovered_ranges[0].low * 4000000 + y

    raise RuntimeError("Could not find distress beacon")
