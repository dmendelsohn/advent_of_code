from pathlib import Path
from typing import List, NamedTuple, Optional, Set

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"


class Point(NamedTuple):
    x: int
    y: int
    z: int


class Interval(NamedTuple):
    low: int
    high: int

    def clamp(self, other: "Interval") -> Optional["Interval"]:
        """ Return just the portion of this interval within the other interval """
        low = max(self.low, other.low)
        high = min(self.high, other.high)
        return Interval(low, high) if low <= high else None

    def get_offcuts(self, other: "Interval") -> Set["Interval"]:
        """ Cut away parts of this interval that don't overlap other """
        offcuts = set()
        if self.low < other.low:
            offcuts.add(Interval(self.low, min(self.high, other.low - 1)))
        if self.high > other.high:
            offcuts.add(Interval(max(self.low, other.high + 1), self.high))
        return offcuts

    def __len__(self) -> int:
        return self.high - self.low + 1


class Box(NamedTuple):
    x_int: Interval
    y_int: Interval
    z_int: Interval

    def clamp(self, other: "Box") -> Optional["Box"]:
        """ Return just the portion of this box within the other box """
        x_int = self.x_int.clamp(other.x_int)
        y_int = self.y_int.clamp(other.y_int)
        z_int = self.z_int.clamp(other.z_int)
        return Box(x_int, y_int, z_int) if x_int and y_int and z_int else None

    def mask(self, other: "Box") -> Set["Box"]:
        """
        Emit 1 or more boxes resulting from cutting out the other box
        Strategy: cut off boxes from self until other is all that is left
        """
        other = other.clamp(self)
        if not other:
            # No intersection
            return {self}

        # Otherwise, carve out pieces of self until just other is left
        remaining = self
        offcuts = set()

        # x off cuts
        offcut_ints = remaining.x_int.get_offcuts(other.x_int)
        offcuts.update(Box(offcut_int, remaining.y_int, remaining.z_int) for offcut_int in offcut_ints)
        remaining = Box(other.x_int, remaining.y_int, remaining.z_int)

        # y off cuts
        offcut_ints = remaining.y_int.get_offcuts(other.y_int)
        offcuts.update(Box(remaining.x_int, offcut_int, remaining.z_int) for offcut_int in offcut_ints)
        remaining = Box(remaining.x_int, other.y_int, remaining.z_int)

        # x off cuts
        offcut_ints = remaining.z_int.get_offcuts(other.z_int)
        offcuts.update(Box(remaining.x_int, remaining.y_int, offcut_int) for offcut_int in offcut_ints)
        remaining = Box(remaining.x_int, remaining.y_int, other.z_int)

        if remaining != other:
            raise RuntimeError(f"Offcuts did not leave us with other\nremaining={remaining}\nother={other}")

        return offcuts

    def size(self) -> int:
        return len(self.x_int) * len(self.y_int) * len(self.z_int)


class RebootStep(NamedTuple):
    state: bool
    box: Box


def get_on_boxes_after_step(on_boxes: Set[Box], step: RebootStep) -> Set[Box]:
    # First mask the new box from all existing boxes
    # Even if the new step is an "on" step, this will help get rid of overlap
    next_on_boxes = set()
    for on_box in on_boxes:
        next_on_boxes.update(on_box.mask(step.box))

    if step.state:
        next_on_boxes.add(step.box)

    return next_on_boxes


def apply_steps(steps: List[RebootStep]) -> Set[Box]:
    """ Return the on-boxes """
    on_boxes = set()
    for step in steps:
        on_boxes = get_on_boxes_after_step(on_boxes, step)
    return on_boxes


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_spec(spec: str) -> Interval:
    spec = spec[2:]  # Strip "x=" etc
    return Interval(*[int(part) for part in spec.split("..")])


def parse_step(line: str) -> RebootStep:
    inst, coords = line.split(" ")
    state = (inst == "on")
    x_int, y_int, z_int = [parse_spec(spec) for spec in coords.split(",")]
    box = Box(x_int, y_int, z_int)
    return RebootStep(state, box)


def parse_input(use_test_input: bool = False) -> List[RebootStep]:
    raw_input = read_input(use_test_input)
    return [parse_step(line) for line in raw_input.split("\n")]


def part_1(use_test_input: bool = False) -> str:
    boundary_box = Box(Interval(-50, 50), Interval(-50, 50), Interval(-50, 50))
    steps = parse_input(use_test_input)
    on_boxes = apply_steps(steps)
    on_boxes = {on_box.clamp(boundary_box) for on_box in on_boxes}
    num_lights = sum(on_box.size() for on_box in on_boxes if on_box)
    return f"{num_lights}"


def part_2(use_test_input: bool = False) -> str:
    steps = parse_input(use_test_input)
    on_boxes = apply_steps(steps)
    num_lights = sum(on_box.size() for on_box in on_boxes)
    return f"{num_lights}"
