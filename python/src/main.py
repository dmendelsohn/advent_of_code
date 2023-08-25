import argparse
import importlib
from pathlib import Path
from typing import Callable, NamedTuple

Solution = Callable[[str], str | int]


class Args(NamedTuple):
    year: int
    day: int
    example: bool


def parse_args() -> Args:
    parser = argparse.ArgumentParser("Advent of Code")
    parser.add_argument("-y", "--year", dest="year", type=int, default=2019)
    parser.add_argument("-d", "--day", dest="day", type=int)
    parser.add_argument("-e", "--example", dest="example", action="store_true")
    args = parser.parse_args()
    return Args(year=args.year, day=args.day, example=args.example)


def get_input(args: Args) -> str:
    input_dir = Path(__file__).parent.parent.parent / "inputs" / f"year{args.year:04d}"
    filename = f"example{args.day:02d}.txt" if args.example else f"day{args.day:02d}.txt"
    path = input_dir / filename
    return path.read_text().strip()


def get_implementation(args: Args) -> tuple[Solution, Solution]:
    solution_module = importlib.import_module(f"year{args.year:04d}.day{args.day:02d}.solution")
    return getattr(solution_module, "part_1"), getattr(solution_module, "part_2")


def main():
    args = parse_args()
    input_text = get_input(args)
    part1, part2 = get_implementation(args)

    print(f"{'[EXAMPLE] 'if args.example else ''}Running {args.year} Day {args.day:02d}")
    print(f"Part 1: {part1(input_text)}")
    print(f"Part 2: {part2(input_text)}")


if __name__ == "__main__":
    main()
