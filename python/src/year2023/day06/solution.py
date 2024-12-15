import math
from dataclasses import dataclass


@dataclass
class Race:
    time: int
    goal: int

    @property
    def ways_to_win(self) -> int:
        """
        Let x be the number of seconds we hold the button
        To match or exceed the goal:
            x * (time - x) >= goal
        Rearrange:
            x^2 - (time) * x + G <= 0
        Solve for the zeros, and all values in between will be ways
        to win because the quadratic is concave down.
        """
        discriminant = self.time**2 - 4 * self.goal
        if discriminant < 0:
            return 0

        max_zero = 0.5 * (self.time + math.sqrt(discriminant))
        min_zero = 0.5 * (self.time - math.sqrt(discriminant))
        max_winning_int = math.floor(max_zero)
        min_winning_int = max(0, math.ceil(min_zero))

        # Matching the goal exactly doesn't count as winning
        if max_winning_int * (self.time - max_winning_int) == self.goal:
            max_winning_int -= 1
        if min_winning_int * (self.time - min_winning_int) == self.goal:
            min_winning_int += 1

        ways_to_win = max(0, max_winning_int - min_winning_int + 1)
        return max(ways_to_win, 0)


def part_1(puzzle_input: str) -> str | int:
    time_line, goal_line = puzzle_input.split("\n")
    times = list(map(int, time_line.split()[1:]))
    goals = list(map(int, goal_line.split()[1:]))
    races = [Race(time, goal) for time, goal in zip(times, goals)]
    product = 1
    for race in races:
        product *= race.ways_to_win
    return product


def part_2(puzzle_input: str) -> str | int:
    time_line, goal_line = puzzle_input.split("\n")
    time = int("".join(c for c in time_line if c.isdigit()))
    goal = int("".join(c for c in goal_line if c.isdigit()))
    race = Race(time, goal)
    return race.ways_to_win
