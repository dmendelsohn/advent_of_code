from typing import Optional


def parse_line(line: str) -> Optional[int]:
    if line == "noop":
        return None
    else:
        _, num = line.split(" ")
        return int(num)


def parse_input(text: str) -> list[Optional[int]]:
    return [parse_line(line) for line in text.split("\n")]


def execute_instructions(instructions: list[Optional[int]]) -> list[int]:
    # Return array[i] is value of register DURING cycle i
    register_vals = [1, 1]
    for instruction in instructions:
        register_vals.append(register_vals[-1])
        if instruction is not None:
            register_vals.append(register_vals[-1] + instruction)
    return register_vals


def part_1(puzzle_input: str) -> str | int:
    register_vals = execute_instructions(parse_input(puzzle_input))
    output = 0
    for cycle in range(20, len(register_vals), 40):
        output += cycle * register_vals[cycle]
    return output


def part_2(puzzle_input: str) -> str | int:
    register_vals = execute_instructions(parse_input(puzzle_input))
    buffer: list[list[str]] = [[] for _ in range(6)]  # Each line starts as an empty list
    for cycle in range(1, 241):
        row = (cycle - 1) // 40
        column = (cycle - 1) % 40
        if abs(register_vals[cycle] - column) <= 1:
            buffer[row].append("#")
        else:
            buffer[row].append(".")

    return "\n" + "\n".join("".join(row) for row in buffer)
