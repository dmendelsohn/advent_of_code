import itertools
from dataclasses import dataclass
from functools import reduce


@dataclass(frozen=True)
class Range:
    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length - 1

    def overlap(self, other: "Range") -> "Range | None":
        if self.start > other.end:
            # No overlap
            return None
        if other.start > self.end:
            # No overlap
            return None

        overlap_start = max(self.start, other.start)
        overlap_end = min(self.end, other.end)
        overlap_length = overlap_end - overlap_start + 1
        return Range(overlap_start, overlap_length)


@dataclass(frozen=True)
class RangeMapEntry:
    src_start: int
    dest_start: int
    length: int

    @property
    def src_range(self) -> Range:
        return Range(self.src_start, self.length)


@dataclass
class RangeMap:
    entries: set[RangeMapEntry]

    @classmethod
    def from_section(cls, text: str) -> "RangeMap":
        # Skip header line
        entries: set[RangeMapEntry] = set()
        for line in text.split("\n")[1:]:
            dest_start, src_start, length = map(int, line.split())
            entries.add(RangeMapEntry(src_start, dest_start, length))
        return cls(entries)

    def apply(self, src_value: int) -> int:
        for entry in self.entries:
            if 0 <= (offset := src_value - entry.src_start) < entry.length:
                return entry.dest_start + offset
        return src_value

    def apply_range(self, src_range: Range) -> set[Range]:
        range_mappings: dict[Range, Range] = {}
        for entry in sorted(self.entries, key=lambda entry: entry.src_start):
            if (overlap := entry.src_range.overlap(src_range)) is not None:
                offset = overlap.start - entry.src_start
                range_mappings[overlap] = Range(entry.dest_start + offset, overlap.length)

        # Let's not forget subranges of the unmapped input range that are unmapped
        # Those ranges should pass through unchanged
        # Add a dummy range before and after src_range to serve as bookends for finding gaps
        mapped_src_ranges = sorted(range_mappings.keys(), key=lambda r: r.start)
        mapped_src_ranges.insert(0, Range(src_range.start - 1, 1))
        mapped_src_ranges.append(Range(src_range.end + 1, 1))
        unmapped_ranges: set[Range] = set()
        for idx in range(len(mapped_src_ranges) - 1):
            gap_length = mapped_src_ranges[idx + 1].start - mapped_src_ranges[idx].end - 1
            if gap_length > 0:
                unmapped_ranges.add(Range(mapped_src_ranges[idx].end + 1, gap_length))

        return set(range_mappings.values()) | unmapped_ranges


def parse_input(puzzle_input: str) -> tuple[list[int], list[RangeMap]]:
    seed_section, *map_sections = puzzle_input.split("\n\n")
    seeds = [int(part) for part in seed_section.split() if part.isdigit()]
    range_maps = [RangeMap.from_section(section) for section in map_sections]
    return seeds, range_maps


def get_location(seed: int, range_maps: list[RangeMap]) -> int:
    return reduce(lambda val, range_map: range_map.apply(val), range_maps, seed)


def get_location_ranges(seed_range: Range, range_maps: list[RangeMap]) -> set[Range]:
    return reduce(
        lambda ranges, range_map: set(itertools.chain(*(range_map.apply_range(r) for r in ranges))),
        range_maps,
        {seed_range},
    )


def part_1(puzzle_input: str) -> str | int:
    seeds, range_maps = parse_input(puzzle_input)
    return min(get_location(seed, range_maps) for seed in seeds)


def part_2(puzzle_input: str) -> str | int:
    seed_vals, range_maps = parse_input(puzzle_input)
    location_ranges: set[Range] = set()
    for idx in range(len(seed_vals) // 2):
        seed_range = Range(seed_vals[2 * idx], seed_vals[2 * idx + 1])
        location_ranges.update(get_location_ranges(seed_range, range_maps))

    return min(r.start for r in location_ranges)
