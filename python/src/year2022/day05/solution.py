import re
from typing import NamedTuple

Stacks = list[list[str]]


def parse_initial_stacks(text: str) -> Stacks:
    lines = text.split("\n")

    # Count the number of stacks
    stack_ids = [int(char) for char in lines[-1] if not char.isspace()]
    num_stacks = len(stack_ids)
    assert stack_ids == list(range(1, 1 + num_stacks))

    stacks: Stacks = [[] for _ in range(num_stacks)]

    for line_idx in range(len(lines) - 2, -1, -1):
        line = lines[line_idx]
        for stack_idx in range(num_stacks):
            char_idx = 4 * stack_idx + 1
            if char_idx < len(line) and not line[char_idx].isspace():
                stacks[stack_idx].append(line[char_idx])

    return stacks


class Instruction(NamedTuple):
    source: int
    target: int
    num: int


def parse_instructions(text: str) -> list[Instruction]:
    instructions = []
    for line in text.split("\n"):
        match = re.match(r"move (\d+) from (\d+) to (\d+)", line)
        if not match:
            raise ValueError(f"Could not parse instruction: {line}")
        num, source, target = map(int, match.groups())
        # Convert to 0-indexing
        instructions.append(Instruction(source - 1, target - 1, num))
    return instructions


def parse_input(text: str) -> tuple[Stacks, list[Instruction]]:
    stacks_text, instructions_text = text.split("\n\n")
    return parse_initial_stacks(stacks_text), parse_instructions(instructions_text)


def apply_instruction_part_1(stacks: Stacks, instruction: Instruction) -> None:
    for _ in range(instruction.num):
        stacks[instruction.target].append(stacks[instruction.source].pop())


def apply_instruction_part_2(stacks: Stacks, instruction: Instruction) -> None:
    temp_stack = []
    for _ in range(instruction.num):
        temp_stack.append(stacks[instruction.source].pop())
    for _ in range(instruction.num):
        stacks[instruction.target].append(temp_stack.pop())


def part_1(puzzle_input: str) -> str | int:
    stacks, instructions = parse_input(puzzle_input)
    for instruction in instructions:
        apply_instruction_part_1(stacks, instruction)
    return "".join(stack[-1] for stack in stacks)


def part_2(puzzle_input: str) -> str | int:
    stacks, instructions = parse_input(puzzle_input)
    for instruction in instructions:
        apply_instruction_part_2(stacks, instruction)
    return "".join(stack[-1] for stack in stacks)
