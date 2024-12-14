def part_1_value(line: str) -> int:
    digits = [int(chr) for chr in line if chr in "0123456789"]
    return 10 * digits[0] + digits[-1]


def part_1(puzzle_input: str) -> str | int:
    return sum(part_1_value(line) for line in puzzle_input.split("\n"))


def part_2_value(line: str) -> int:
    encodings = {str(digit): digit for digit in range(10)}
    encodings.update(
        {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
        }
    )
    digits = []
    for idx in range(len(line)):
        for encoding, value in encodings.items():
            if line[idx : idx + len(encoding)] == encoding:
                digits.append(value)
    return 10 * digits[0] + digits[-1]


def part_2(puzzle_input: str) -> str | int:
    return sum(part_2_value(line) for line in puzzle_input.split("\n"))
