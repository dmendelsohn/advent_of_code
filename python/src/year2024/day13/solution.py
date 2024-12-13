import re
from dataclasses import dataclass

SECTION_REGEX = re.compile(
    r"""Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)"""
)

PART_2_FACTOR = 10**13


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)


@dataclass
class Game:
    a_press: Vector
    b_press: Vector
    goal: Vector

    @classmethod
    def from_section(cls, section: str, goal_offset: Vector = Vector(0, 0)) -> "Game":
        if (match := re.search(SECTION_REGEX, section)) is None:
            raise ValueError(f"Could not parse section: {section}")
        a_x, a_y, b_x, b_y, goal_x, goal_y = map(int, match.groups())
        return Game(Vector(a_x, a_y), Vector(b_x, b_y), Vector(goal_x, goal_y) + goal_offset)

    def get_min_cost(self) -> int | None:
        # Solve by inverting the "press matrix" and multiply by the goal vector
        discriminant = self.a_press.x * self.b_press.y - self.a_press.y * self.b_press.x
        if discriminant == 0:
            raise ValueError("Cannot solve by inversion when matrix has 0 discriminant")

        a_count = self.b_press.y * self.goal.x - self.b_press.x * self.goal.y
        if a_count % discriminant != 0:
            return None
        a_count //= discriminant

        b_count = -self.a_press.y * self.goal.x + self.a_press.x * self.goal.y
        if b_count % discriminant != 0:
            return None
        b_count //= discriminant

        return 3 * a_count + b_count


def part_1(puzzle_input: str) -> str | int:
    games = [Game.from_section(section) for section in puzzle_input.split("\n\n")]
    return sum(cost for game in games if (cost := game.get_min_cost()) is not None)


def part_2(puzzle_input: str) -> str | int:
    goal_offset = Vector(PART_2_FACTOR, PART_2_FACTOR)
    games = [Game.from_section(section, goal_offset) for section in puzzle_input.split("\n\n")]
    return sum(cost for game in games if (cost := game.get_min_cost()) is not None)
