def parse_input(text: str) -> list[int]:
    return [int(num) for num in text.split(",")]


def run_program(program: list[int], pc: int) -> None:
    while program[pc] != 99:
        a, b, c = program[pc + 1 : pc + 4]
        if program[pc] == 1:
            program[c] = program[a] + program[b]
        elif program[pc] == 2:
            program[c] = program[a] * program[b]
        else:
            raise ValueError(f"Invalid opcode {program[pc]}")
        pc += 4


def part_1(puzzle_input: str) -> str | int:
    program = parse_input(puzzle_input)
    program[1:3] = [12, 2]
    run_program(program, 0)
    return program[0]


def part_2(puzzle_input: str) -> str | int:
    program = parse_input(puzzle_input)
    for i in range(100):
        for j in range(100):
            program_copy = program[:]
            program_copy[1:3] = [i, j]
            run_program(program_copy, 0)
            if program_copy[0] == 19690720:
                return 100 * i + j
    raise RuntimeError("Could not find answer")
