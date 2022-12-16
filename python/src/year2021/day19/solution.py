from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
from numpy.linalg import matrix_power

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"


ReadingSet = np.array  # Nx3 2D array
Rotation = np.array  # 3x3 2D array
Translation = np.array  # 1x3 2D array
Vector = np.array  # Length 3 1D array


@lru_cache()
def get_rotations() -> List[Rotation]:
    eye = np.eye(3)
    x_90 = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]])
    y_90 = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]])
    z_90 = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])
    face_rots = [
        eye,
        x_90,
        matrix_power(x_90, 2),
        matrix_power(x_90, 3),
        y_90,
        matrix_power(y_90, 3),
    ]
    orientation_rots = [eye, z_90, matrix_power(z_90, 2), matrix_power(z_90, 3)]
    rotations = []
    for f in face_rots:
        for o in orientation_rots:
            rotations.append(np.matmul(f, o))
    return rotations


def rotate_reading_set(reading_set: ReadingSet, rotation: Rotation) -> ReadingSet:
    return np.matmul(reading_set, rotation)


def translate_reading_set(reading_set: ReadingSet, translation: Translation) -> ReadingSet:
    translation_matrix = np.repeat(translation, len(reading_set), axis=0)
    return reading_set + translation_matrix


def count_overlap(first: ReadingSet, second: ReadingSet) -> int:
    # Assumes no duplicates within each set
    return len(first) + len(second) - len(merge_reading_sets([first, second]))


def merge_reading_sets(reading_sets: Iterable[ReadingSet]) -> ReadingSet:
    """Combine the input reading sets, deduplicated overlapping points"""
    stacked = np.vstack(list(reading_sets))
    return np.unique(stacked, axis=0)


def align_reading_set(
    this: ReadingSet, ref: ReadingSet
) -> Optional[Tuple[ReadingSet, Rotation, Translation]]:
    """
    Try rotation and translations of this reading set to see if we can get 12-point overlap
      with the ref reading set.
    If so, return a merged reading set with the entire ref set and the rotated + aligned
      version of this set.
    If not, return None.
    If there are multiple ways to align, we pick one arbitrarily.
    """
    for rotation in get_rotations():
        rotated_reading_set = rotate_reading_set(this, rotation)
        result = align_reading_set_translate(rotated_reading_set, ref)
        if result is not None:
            aligned_reading_set, translation = result
            return aligned_reading_set, rotation, translation
    return None


def align_reading_set_translate(
    this: ReadingSet, ref: ReadingSet
) -> Optional[Tuple[ReadingSet, Translation]]:
    """
    Try just translations of this reading set to see if we can get 12-point overlap
      with the ref reading set.
    If so, return a copy of this reading set translated into the other reading set's frame
    If not, return None
    If there are multiple ways to align, we pick one arbitrarily
    """
    for this_row_idx in range(len(this)):
        for ref_row_idx in range(len(ref)):
            # Translate `this` so that the selected row in `this` matches the selected for in `ref`
            translation = (
                ref[ref_row_idx : ref_row_idx + 1, :] - this[this_row_idx : this_row_idx + 1, :]
            )
            translated_this = translate_reading_set(this, translation)

            # If we find 12 overlapping points, we're done
            num_overlap = count_overlap(translated_this, ref)
            if num_overlap >= 12:
                return translated_this, translation
    return None


def align_all_reading_sets(
    scanner_to_reading_set: Dict[int, ReadingSet], start_ref_scanner: int
) -> Dict[int, Vector]:
    """Updates scanner_to_reading_set input in place, and returns scanner locations"""
    aligned_scanners = {start_ref_scanner}
    align_to_queue = [start_ref_scanner]
    scanner_locations = {start_ref_scanner: np.zeros((3,), dtype=int)}
    while align_to_queue:
        # Pick reference scanner from front of FIFO queue
        ref_scanner = align_to_queue.pop(0)
        ref_reading_set = scanner_to_reading_set[ref_scanner]

        # Try to align each remaining unaligned scanner to it
        unaligned_scanners = set(scanner_to_reading_set.keys()) - aligned_scanners
        for unaligned_scanner in unaligned_scanners:
            unaligned_reading_set = scanner_to_reading_set[unaligned_scanner]
            result = align_reading_set(unaligned_reading_set, ref_reading_set)
            if result is not None:
                aligned_reading_set, rotation, translation = result
                # Found an alignment! Add this scanner to the align_to_queue and update tracker vars
                print(f"Found an alignment ({unaligned_scanner} to {ref_scanner})")
                scanner_to_reading_set[unaligned_scanner] = aligned_reading_set
                aligned_scanners.add(unaligned_scanner)
                align_to_queue.append(unaligned_scanner)
                scanner_locations[unaligned_scanner] = (
                    np.matmul(np.zeros((3,), dtype=int), rotation) + translation
                )

    unaligned_scanners = set(scanner_to_reading_set.keys()) - aligned_scanners
    if unaligned_scanners:
        raise RuntimeError(f"Could not align scanners: {unaligned_scanners}")

    return scanner_locations


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read()


def parse_input(use_test_input: bool = False) -> Dict[int, ReadingSet]:
    """Return mapping from scanner number to ReadingSet"""
    raw_input = read_input(use_test_input)
    scanner_to_reading_set = dict()
    current_scanner = None
    current_reading_set = []
    # Could do regexes here, but meh
    for line in raw_input.split("\n"):
        line = line.strip()
        if not line:
            # "Commit" current scanner readings
            if current_reading_set:
                scanner_to_reading_set[current_scanner] = np.array(current_reading_set)
                current_scanner = None
                current_reading_set = []
        elif "scanner" in line:
            current_scanner = int(line.split(" ")[2])
        else:
            x, y, z = [int(part) for part in line.split(",")]
            current_reading_set.append((x, y, z))
    return scanner_to_reading_set


def part_1(use_test_input: bool = False) -> str:
    scanner_to_reading_set = parse_input(use_test_input)
    align_all_reading_sets(scanner_to_reading_set, 0)
    merged_reading_set = merge_reading_sets(scanner_to_reading_set.values())
    num_distinct = len(merged_reading_set)
    return f"{num_distinct}"


def get_taxicab_dist(first: Vector, second: Vector) -> int:
    return int(np.sum(np.absolute(first - second)))


def part_2(use_test_input: bool = False) -> str:
    scanner_to_reading_set = parse_input(use_test_input)
    scanner_locations = align_all_reading_sets(scanner_to_reading_set, 0)
    max_dist = 0
    for first_scanner, first_vector in scanner_locations.items():
        for second_scanner, second_vector in scanner_locations.items():
            dist = get_taxicab_dist(first_vector, second_vector)
            if dist > max_dist:
                max_dist = dist
                print(
                    f"Found new max of {dist} "
                    f"({first_scanner} at {first_vector} to {second_scanner} at {second_vector}"
                )
    return f"{max_dist}"
