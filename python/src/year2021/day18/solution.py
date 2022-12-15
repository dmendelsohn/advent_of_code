from pathlib import Path
from typing import List, Tuple, Union

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"


Token = Union[int, str]  # str is one of "[" or "]" or ","
Expression = List[Token]


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_expression(string: str) -> Expression:
    expression = []
    for char in string:
        if char in ",[]":
            expression.append(char)
        elif char in "0123456789":
            expression.append(int(char))
    return expression


def print_expression(expression: Expression) -> None:
    print("".join(str(token) for token in expression))


def parse_input(use_test_input: bool = False) -> List[Expression]:
    raw_input = read_input(use_test_input)
    return [parse_expression(line.strip()) for line in raw_input.split("\n")]


def explode(expr: Expression, i: int) -> Expression:
    # i is index of start of the pair which should be a left paren token
    left_num = expr[i + 1]
    right_num = expr[i + 3]
    left_expr = expr[:i]
    right_expr = expr[i + 5:]
    insert_expr = [0]

    # Add left num
    j = len(left_expr) - 1
    while j >= 0:
        if isinstance(left_expr[j], int):
            left_expr[j] += left_num
            break
        j -= 1

    # Add right num
    j = 0
    while j < len(right_expr):
        if isinstance(right_expr[j], int):
            right_expr[j] += right_num
            break
        j += 1

    return left_expr + insert_expr + right_expr


def split(expr: Expression, i: int) -> Expression:
    # i is index of big number to be split
    num = expr[i]
    left_expr = expr[:i]
    right_expr = expr[i+1:]
    insert_expr = ["[", num // 2, ",", (num + 1) // 2, "]"]
    return left_expr + insert_expr + right_expr


def reduce(expr: Expression) -> Expression:
    # First look for a pair to explode (found when we see 5 more [ than ] )
    left_unbalance = 0
    for i, token in enumerate(expr):
        if token == "[":
            left_unbalance += 1
        elif token == "]":
            left_unbalance -= 1
        if left_unbalance == 5:
            return explode(expr, i)

    # Now look for something to split
    for i, token in enumerate(expr):
        if isinstance(token, int) and token >= 10:
            return split(expr, i)

    return expr


def add(left: Expression, right: Expression) -> Expression:
    result = ["["] + left + [","] + right + ["]"]
    reduced_result = reduce(result)
    while reduced_result != result:
        result = reduced_result
        reduced_result = reduce(result)
    return reduced_result


def decompose(expr: Expression) -> Tuple[Expression, Expression]:
    left_unbalance = 0
    for i, token in enumerate(expr):
        if token == "[":
            left_unbalance += 1
        elif token == "]":
            left_unbalance -= 1

        if left_unbalance == 1 and token == ",":
            return expr[1:i], expr[i+1:-1]

    raise RuntimeError(f"Could not decompose {expr}")


def magnitude(expr: Expression) -> int:
    if len(expr) == 1:
        if not isinstance(expr[0], int):
            raise ValueError(f"Cannot get magnitude of {expr}")
        return expr[0]
    left_expr, right_expr = decompose(expr)
    return 3 * magnitude(left_expr) + 2 * magnitude(right_expr)


def part_1(use_test_input: bool = False) -> str:
    expressions = parse_input(use_test_input)
    result = expressions[0]
    for next_expr in expressions[1:]:
        result = add(result, next_expr)
    print_expression(result)
    return f"{magnitude(result)}"


def part_2(use_test_input: bool = False) -> str:
    largest_mag = 0
    expressions = parse_input(use_test_input)
    for left in expressions:
        for right in expressions:
            if left == right:
                continue
            result = add(left[:], right[:])
            mag = magnitude(result[:])
            if mag > largest_mag:
                largest_mag = mag
    return f"{largest_mag}"
