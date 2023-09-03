def decode_digit(digit: str) -> int:
    return {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2}[digit]


def decode(snafu: str) -> int:
    """Decode SNAFU number"""
    place = 1
    total = 0
    for digit in reversed(snafu):
        total += place * decode_digit(digit)
        place *= 5
    return total


def encode_digit(num: int) -> str:
    return {0: "0", 1: "1", 2: "2", -1: "-", -2: "="}[num]


def encode(num: int) -> str:
    """Encode SNAFU number"""
    digits = []  # Encoded digits (in reverse)
    while num:
        lowest_digit_value = ((num + 2) % 5) - 2
        digits.append(encode_digit(lowest_digit_value))
        num = (num - lowest_digit_value) // 5
    return "".join(reversed(digits))


def part_1(puzzle_input: str) -> str | int:
    return encode(sum(decode(line) for line in puzzle_input.split("\n")))


def part_2(puzzle_input: str) -> str | int:
    return "N/A - freebie"
