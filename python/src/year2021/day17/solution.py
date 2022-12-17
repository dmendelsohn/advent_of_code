import re
from pathlib import Path
from typing import Any, NamedTuple, Set

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"


class TargetBox(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(self, other: Any) -> "Vector":
        if not isinstance(other, Vector):
            raise ValueError(f"other must be a Vector, not {type(other)}")
        return Vector(self.x + other.x, self.y + other.y)


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_input(use_test_input: bool = False) -> TargetBox:
    raw_input = read_input(use_test_input)
    pattern = r"^target area: x=(-?[0-9]+)\.\.(-?[0-9]+), y=(-?[0-9]+)\.\.(-?[0-9]+)$"
    groups = re.match(pattern, raw_input).groups()  # type: ignore
    return TargetBox(*(int(val) for val in groups))


def part_1(use_test_input: bool = False) -> str:
    target_box = parse_input(use_test_input)
    if target_box.max_y >= 0:
        raise NotImplementedError
    init_y = abs(target_box.min_y) - 1
    max_height = init_y * (init_y + 1) // 2
    return f"{max_height}"


def get_first_triangle_num_in_range(min_val: int, max_val: int) -> int:
    total = 0
    n = 0
    while total < min_val:
        n += 1
        total += n
    if total > max_val:
        raise ValueError("No triangle number in range")
    return n


def is_on_target_launch(target_box: TargetBox, launch: Vector) -> bool:
    pos = Vector(0, 0)
    vel = launch
    while True:
        if (
            target_box.min_x <= pos.x <= target_box.max_x
            and target_box.min_y <= pos.y <= target_box.max_y
        ):
            return True  # Hit the target
        if pos.x > target_box.max_x or pos.y < target_box.min_y:
            return False  # Passed the target
        # Update position and velocity
        pos += vel
        vel = Vector(max(vel.x - 1, 0), vel.y - 1)


def get_on_target_launches(target_box: TargetBox) -> Set[Vector]:
    if target_box.max_y >= 0 or target_box.min_x <= 0:
        raise NotImplementedError
    launch_x_min = get_first_triangle_num_in_range(target_box.min_x, target_box.max_x)
    launch_x_max = target_box.max_x
    launch_y_min = target_box.min_y
    launch_y_max = -1 * target_box.min_y - 1
    on_target_vectors = set()
    for launch_x in range(launch_x_min, launch_x_max + 1):
        for launch_y in range(launch_y_min, launch_y_max + 1):
            launch_vector = Vector(launch_x, launch_y)
            if is_on_target_launch(target_box, launch_vector):
                on_target_vectors.add(launch_vector)
    return on_target_vectors


def part_2(use_test_input: bool = False) -> str:
    target_box = parse_input(use_test_input)
    answer = len(get_on_target_launches(target_box))
    return f"{answer}"
