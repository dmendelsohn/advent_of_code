from pathlib import Path
from typing import Dict, List

INPUT_PATH = Path(__file__).parent / "input.txt"

School = Dict[int, int]  # Dict values are num fish with counter=key


def parse_input() -> List[int]:
    return [int(elt) for elt in open(INPUT_PATH).read().strip().split(",")]


def get_school(fish_counters: List[int]) -> School:
    school = {i: 0 for i in range(9)}
    for fish_counter in fish_counters:
        school[fish_counter] += 1
    return school


def iterate_school(old_school: School) -> School:
    new_school = {i: 0 for i in range(9)}
    for num_days, num_fish in old_school.items():
        num_days -= 1
        if num_days < 0:
            new_school[6] += num_fish
            new_school[8] += num_fish  # New fish
        else:
            new_school[num_days] += num_fish
    return new_school


def school_size(school: School) -> int:
    return sum(school.values())


def simulate_school(school: School, num_iterations: int) -> int:
    size = school_size(school)
    for i in range(num_iterations):
        school = iterate_school(school)
        size = school_size(school)
        print(f"After {i} days, school size is {size}")
    return size


def part_1() -> str:
    school = get_school(parse_input())
    size = simulate_school(school, 80)
    return f"{size}"


def part_2() -> str:
    school = get_school(parse_input())
    size = simulate_school(school, 256)
    return f"{size}"
