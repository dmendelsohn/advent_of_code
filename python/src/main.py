import argparse
import importlib


def main(day_num: int, part_num: int, is_test: bool) -> None:
    selected_solution_module = importlib.import_module(f"days.day{day_num:02d}.solution")
    selected_part_func = getattr(selected_solution_module, f"part_{part_num}")
    if day_num < 7:  # Didn't support is_test yet
        solution = selected_part_func()
        if is_test:
            raise ValueError("is_test=True not supported before Day 7")
    else:
        solution = selected_part_func(is_test)
    print(f"{'[TEST] ' if is_test else ''}Day {day_num}, Part {part_num}: {solution}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("TODO")
    parser.add_argument("-d", "--day", dest="day", type=int)
    parser.add_argument("-p", "--part", dest="part", type=int)
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    main(args.day, args.part, args.test)
