import math
from dataclasses import dataclass


@dataclass
class Equation:
    operands: tuple[int, ...]
    result: int

    def is_satisfiable(self, allow_concat: bool) -> bool:
        if len(self.operands) == 1:
            return self.operands[0] == self.result

        partial_operands = self.operands[:-1]
        if (sub_result := self.result - self.operands[-1]) >= 0:
            if Equation(partial_operands, sub_result).is_satisfiable(allow_concat):
                return True

        dividend, remainder = divmod(self.result, self.operands[-1])
        if remainder == 0:
            if Equation(partial_operands, dividend).is_satisfiable(allow_concat):
                return True

        if allow_concat:
            num_suffix_digits = (
                int(math.log10(self.operands[-1])) + 1 if self.operands[-1] > 0 else 1
            )
            dividend, remainder = divmod(self.result, 10**num_suffix_digits)
            if remainder == self.operands[-1]:
                if Equation(partial_operands, dividend).is_satisfiable(allow_concat):
                    return True

        return False

    @classmethod
    def from_line(cls, line: str) -> "Equation":
        left, right = line.split(": ")
        result = int(left)
        operands = tuple(int(num) for num in right.split())
        return Equation(operands, result)


def part_1(puzzle_input: str) -> str | int:
    equations = [Equation.from_line(line) for line in puzzle_input.split("\n")]
    return sum(eq.result for eq in equations if eq.is_satisfiable(False))


def part_2(puzzle_input: str) -> str | int:
    equations = [Equation.from_line(line) for line in puzzle_input.split("\n")]
    return sum(eq.result for eq in equations if eq.is_satisfiable(True))
