def parse_input(text: str) -> list[int]:
    return [int(line) for line in text.split("\n")]


def part_1(puzzle_input: str) -> str | int:
    nums = parse_input(puzzle_input)
    return sum(num // 3 - 2 for num in nums)


def get_required_fuel(mass: int) -> int:
    total_fuel = 0
    while mass:
        added_fuel = mass // 3 - 2
        if added_fuel <= 0:
            break
        total_fuel += added_fuel
        mass = added_fuel
    return total_fuel


def part_2(puzzle_input: str) -> str | int:
    nums = parse_input(puzzle_input)
    return sum(get_required_fuel(mass) for mass in nums)
