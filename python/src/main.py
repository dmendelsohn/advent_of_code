import argparse
import importlib
import time
from pathlib import Path
from typing import Callable, NamedTuple

Solution = Callable[[str], str | int]


class Args(NamedTuple):
    year: int
    day: int
    example: bool


def parse_args() -> Args:
    parser = argparse.ArgumentParser("Advent of Code")
    parser.add_argument("-y", "--year", dest="year", type=int)
    parser.add_argument("-d", "--day", dest="day", type=int)
    parser.add_argument("-e", "--example", dest="example", action="store_true")
    args = parser.parse_args()
    return Args(year=args.year, day=args.day, example=args.example)


def get_input(args: Args, part: int) -> str:
    input_dir = Path(__file__).parent.parent.parent / "inputs" / f"year{args.year:04d}"

    # Try version with suffix e.g. _p1 first, fallback on normal version
    filename = (
        f"example{args.day:02d}_p{part}.txt" if args.example else f"day{args.day:02d}_p{part}.txt"
    )
    path = input_dir / filename
    if not path.exists():
        # Try without _p1 / _p2 suffix
        filename = f"example{args.day:02d}.txt" if args.example else f"day{args.day:02d}.txt"
        path = input_dir / filename

    return path.read_text().rstrip("\n")


def get_implementation(args: Args) -> tuple[Solution, Solution]:
    solution_module = importlib.import_module(f"year{args.year:04d}.day{args.day:02d}.solution")
    return getattr(solution_module, "part_1"), getattr(solution_module, "part_2")


def run_solution(solution: Solution, input_text: str, label: str) -> None:
    start_time = time.time()
    result = solution(input_text)
    duration = time.time() - start_time
    print(f"{label}: {result} (in {duration:.3f}s)")


def main():
    args = parse_args()
    part1_input, part2_input = get_input(args, 1), get_input(args, 2)
    part1, part2 = get_implementation(args)

    print(f"{'[EXAMPLE] 'if args.example else ''}Running {args.year} Day {args.day:02d}")
    run_solution(part1, part1_input, "Part 1")
    run_solution(part2, part2_input, "Part 2")


if __name__ == "__main__":
    main()
