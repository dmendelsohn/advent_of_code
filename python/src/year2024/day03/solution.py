import re


def part_1(puzzle_input: str) -> str | int:
    total = 0
    for match in re.finditer(r"mul\(([\d]+),([\d]+)\)", puzzle_input):
        total += int(match.groups()[0]) * int(match.groups()[1])
    return total


def part_2(puzzle_input: str) -> str | int:
    total = 0
    on = True
    for match in re.finditer(r"(do\(\))|(don't\(\))|mul\(([\d]+),([\d]+)\)", puzzle_input):
        if match.group() == "do()":
            on = True
        elif match.group() == "don't()":
            on = False
        elif on:
            total += int(match.groups()[2]) * int(match.groups()[3])
    return total
