from pathlib import Path
from typing import List

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_input(use_test_input: bool = False) -> List[str]:
    raw_input = read_input(use_test_input)
    return raw_input.split("\n")


def part_1(use_test_input: bool = False) -> str:
    pass


def part_2(use_test_input: bool = False) -> str:
    pass
