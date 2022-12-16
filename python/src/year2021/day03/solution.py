from collections import Counter
from pathlib import Path
from typing import List

INPUT_PATH = Path(__file__).parent / "input.txt"


def parse_input() -> List[str]:
    return open(INPUT_PATH).read().strip().split("\n")


def get_counter_at_position(lines: List[str], pos: int) -> Counter:
    return Counter(line[pos] for line in lines)


def get_num_from_bits(bits: List[str]) -> int:
    return int("".join(bits), 2)


def part_1() -> str:
    lines = parse_input()
    gamma_bits = []
    epsilon_bits = []
    for i in range(len(lines[0])):
        counter = get_counter_at_position(lines, i)
        gamma_bits.append(counter.most_common()[0][0])
        epsilon_bits.append(counter.most_common()[-1][0])

    gamma = get_num_from_bits(gamma_bits)
    epsilon = get_num_from_bits(epsilon_bits)
    return f"{gamma * epsilon}"


def count_zeros_at_pos(binary_strs: List[str], pos: int) -> int:
    return sum(1 for binary_str in binary_strs if binary_str[pos] == "0")


def get_most_common_at_pos(binary_strs: List[str], pos: int) -> str:
    num_zeros = count_zeros_at_pos(binary_strs, pos)
    num_ones = len(binary_strs) - num_zeros
    return "0" if num_zeros > num_ones else "1"


def filter_binaries(binary_strs: List[str], pos: int, match_digit: str) -> List[str]:
    return [binary for binary in binary_strs if binary[pos] == match_digit]


def iterative_filter(binary_strs: List[str], is_min_filter: bool) -> str:
    for pos in range(len(binary_strs[0])):
        if len(binary_strs) == 1:
            break
        match_digit = get_most_common_at_pos(binary_strs, pos)
        if is_min_filter:
            match_digit = str(1 - int(match_digit))
        binary_strs = filter_binaries(binary_strs, pos, match_digit)

    if len(binary_strs) == 1:
        return binary_strs[0]
    else:
        raise RuntimeError(f"Error while filtering, left with: {binary_strs}")


def part_2() -> str:
    binary_strs = parse_input()
    first_reading_bits = iterative_filter(binary_strs, False)
    first_reading = get_num_from_bits(list(first_reading_bits))
    second_reading_bits = iterative_filter(binary_strs, True)
    second_reading = get_num_from_bits(list(second_reading_bits))
    print(f"First: {first_reading}, Second: {second_reading}")
    return f"{first_reading * second_reading}"
