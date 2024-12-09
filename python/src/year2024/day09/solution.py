from dataclasses import dataclass
from heapq import heapify, heappop, heappush


class ArrayDrive(list[int | None]):
    """Simple array representation of hard drive"""

    @classmethod
    def from_input(cls, input: str) -> "ArrayDrive":
        drive = cls()
        for idx, digit in enumerate(map(int, input)):
            if idx % 2 == 0:
                file_idx = idx // 2
                drive.extend([file_idx] * digit)
            else:
                drive.extend([None] * digit)
        return drive

    @property
    def checksum(self) -> int:
        total = 0
        for idx, num in enumerate(self):
            if num is not None:
                total += idx * num
        return total

    def compress(self) -> None:
        empty_idx = self.index(None)
        move_idx = len(self) - 1
        while move_idx > empty_idx:
            if (move_elt := self[move_idx]) is not None:
                self[empty_idx] = move_elt
                self[move_idx] = None
                empty_idx = self.index(None, empty_idx + 1)
            move_idx -= 1
        del self[empty_idx:]


def part_1(puzzle_input: str) -> str | int:
    drive = ArrayDrive.from_input(puzzle_input)
    drive.compress()
    return drive.checksum


@dataclass
class File:
    id: int
    size: int
    location: int


class MapDrive:
    # File sorted by IDs
    files: list[File]
    # Maps gap size (1-9) to a min heap of gap start indcies
    _gaps: dict[int, list[int]]
    # Indicates if compression has occurred
    _compressed: bool

    def __init__(self, puzzle_input: str):
        # Build up files
        location = 0
        self.files = []
        for idx, size in enumerate(map(int, puzzle_input)):
            if idx % 2 == 0:
                file_idx = idx // 2
                self.files.append(File(id=idx // 2, size=size, location=location))

            location += size

        # Build up the gap index
        self._gaps = {gap_size: [] for gap_size in range(1, 10)}
        for file_idx in range(len(self.files) - 1):
            gap_start = self.files[file_idx].location + self.files[file_idx].size
            gap_size = self.files[file_idx + 1].location - gap_start
            if gap_size > 0:
                self._gaps[gap_size].append(gap_start)
        for heap in self._gaps.values():
            heapify(heap)

        self._compressed = False

    @property
    def checksum(self) -> int:
        total = 0
        for f in self.files:
            total += f.id * sum(range(f.location, f.location + f.size))
        return total

    def compress(self) -> None:
        if self._compressed:
            return None

        # self.files is sorted by file ID
        # Therefore, for uncompressed drives, it is also sorted by file location
        for file_to_move in reversed(self.files):
            candidate_gaps: set[tuple[int, int]] = set()  # Items are (location, gap_size)
            for gap_size in range(file_to_move.size, 10):
                if (
                    self._gaps[gap_size]
                    and (gap_location := self._gaps[gap_size][0]) < file_to_move.location
                ):
                    candidate_gaps.add((gap_location, gap_size))

            if not candidate_gaps:
                # Cannot move the file
                continue

            gap_location, gap_size = min(candidate_gaps)

            # Move the file
            file_to_move.location = gap_location

            # Update gap data structure
            heappop(self._gaps[gap_size])
            if (residual_gap_size := gap_size - file_to_move.size) > 0:
                heappush(self._gaps[residual_gap_size], gap_location + file_to_move.size)

        self._compressed = True


def part_2(puzzle_input: str) -> str | int:
    drive = MapDrive(puzzle_input)
    drive.compress()
    return drive.checksum
