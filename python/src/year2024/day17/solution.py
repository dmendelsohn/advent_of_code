from dataclasses import dataclass
from typing import TypeAlias

Program: TypeAlias = list[int]


@dataclass
class RegisterBank:
    pc: int
    a: int
    b: int
    c: int


def parse_input(puzzle_input: str) -> tuple[RegisterBank, Program]:
    register_section, program_section = puzzle_input.split("\n\n")
    a, b, c = (int(line.split(": ")[1]) for line in register_section.split("\n"))
    registers = RegisterBank(pc=0, a=a, b=b, c=c)
    program = Program(map(int, program_section.split(": ")[1].split(",")))
    return registers, program


def resolve_combo_operand(operand: int, registers: RegisterBank) -> int:
    if operand == 4:
        return registers.a
    if operand == 5:
        return registers.b
    if operand == 6:
        return registers.c
    return operand


def execute_once(registers: RegisterBank, program: Program) -> int | None:
    """
    Execute an instruction, modifying the register bank and returning the output if any
    """
    inst, operand = program[registers.pc : registers.pc + 2]
    output = None
    match inst:
        case 0:
            # adv
            operand = resolve_combo_operand(operand, registers)
            registers.a = registers.a >> operand
        case 1:
            # bxl
            registers.b = registers.b ^ operand
        case 2:
            # bst
            operand = resolve_combo_operand(operand, registers)
            registers.b = operand % 8
        case 3:
            # jnz
            if registers.a != 0:
                registers.pc = operand
            else:
                registers.pc += 2
        case 4:
            # bxc
            registers.b = registers.b ^ registers.c
        case 5:
            # out
            operand = resolve_combo_operand(operand, registers)
            output = operand % 8
        case 6:
            # bdv
            operand = resolve_combo_operand(operand, registers)
            registers.b = registers.a >> operand
        case 7:
            # cdv
            operand = resolve_combo_operand(operand, registers)
            registers.c = registers.a >> operand
        case _:
            raise ValueError(f"Invalid instruction {inst} at pc={registers.pc}")

    if inst != 3:
        registers.pc += 2
    return output


def run_program(registers: RegisterBank, program: Program) -> list[int]:
    outputs: list[int] = []
    while 0 <= registers.pc < len(program):
        if (output := execute_once(registers, program)) is not None:
            outputs.append(output)
    return outputs


def run_hand_compiled_program(a: int) -> list[int]:
    """
    Run an optimized version of the specific program in my input
    Not actually used in the solution, just useful for debugging.
    """
    output: list[int] = []
    while a != 0:
        b = (a % 8) ^ 1
        c = a >> b
        a = a >> 3
        b = b ^ c ^ 4
        output.append(b % 8)
    return output


def get_possible_next_octet(a: int, output: int) -> list[int]:
    """
    Calculate the next 3 bits of a required to produce the requested output
    Hard-codes the algorithm for my specific program input
    """
    possible_octets: list[int] = []
    for octet in range(8):
        b = octet ^ 1
        c = ((a << 3) + octet) >> b
        b = b ^ c ^ 4
        if (b % 8) == output:
            possible_octets.append(octet)

    return possible_octets


def get_quine_start_values(carryin_a: int, outputs: list[int]) -> set[int]:
    if not outputs:
        return {carryin_a}

    *outputs, last_output = outputs
    quine_start_values: set[int] = set()
    for octet in get_possible_next_octet(carryin_a, last_output):
        quine_start_values.update(get_quine_start_values((carryin_a << 3) + octet, outputs))
    return quine_start_values


def part_1(puzzle_input: str) -> str | int:
    registers, program = parse_input(puzzle_input)
    outputs = run_program(registers, program)
    return ",".join(map(str, outputs))


def part_2(puzzle_input: str) -> str | int:
    _, program = parse_input(puzzle_input)
    if len(program) != 16:
        return "Part 2 is not implemented for the example input"

    quine_start_values = get_quine_start_values(0, program)
    return min(quine_start_values)
