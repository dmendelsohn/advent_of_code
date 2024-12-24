import itertools
import random
from dataclasses import dataclass
from typing import TypeAlias


@dataclass(frozen=True)
class BooleanExpression:
    inputs: frozenset[str]
    operator: str

    def __post_init__(self) -> None:
        if len(self.inputs) != 2:
            raise ValueError(f"Expected exactly 2 inputs, not {self.inputs}")


Circuit: TypeAlias = dict[str, BooleanExpression | bool]


def parse_input(puzzle_input: str) -> Circuit:
    constant_section, boolean_section = puzzle_input.split("\n\n")
    circuit: Circuit = {}
    for line in constant_section.split("\n"):
        node, digit_str = line.split(": ")
        circuit[node] = bool(int(digit_str))
    for line in boolean_section.split("\n"):
        expression_str, node = line.split(" -> ")
        left, operator, right = expression_str.split()
        circuit[node] = BooleanExpression(frozenset({left, right}), operator)
    return circuit


class CircuitCycleError(Exception):
    pass


def evaluate_node(
    circuit: Circuit,
    node: str,
    evaluated_nodes: dict[str, bool],
    evaluation_in_progress: set[str] | None = None,
) -> bool:
    if node in evaluated_nodes:
        return evaluated_nodes[node]

    expression = circuit[node]
    if isinstance(expression, bool):
        evaluated_nodes[node] = expression
        return expression
    else:
        evaluation_in_progress = evaluation_in_progress or set()
        if bool(expression.inputs & evaluation_in_progress):
            raise CircuitCycleError

        evaluation_in_progress.add(node)
        left, right = expression.inputs
        evaluate_node(circuit, left, evaluated_nodes, evaluation_in_progress)
        evaluate_node(circuit, right, evaluated_nodes, evaluation_in_progress)
        evaluation_in_progress.remove(node)

        match expression.operator:
            case "AND":
                value = evaluated_nodes[left] and evaluated_nodes[right]
            case "OR":
                value = evaluated_nodes[left] or evaluated_nodes[right]
            case "XOR":
                value = evaluated_nodes[left] != evaluated_nodes[right]
            case _:
                raise ValueError(f"Invalid operation: {expression.operator}")

        evaluated_nodes[node] = value
        return value


def evaluate_circuit(circuit: Circuit) -> int:
    evaluated_nodes: dict[str, bool] = {}
    bits: list[bool] = []
    while (node := f"z{len(bits):02}") in circuit:
        bits.append(evaluate_node(circuit, node, evaluated_nodes))

    output = 0
    for bit in reversed(bits):
        output = 2 * output + int(bit)
    return output


def replace_circuit_inputs(circuit: Circuit, x: int, y: int) -> Circuit:
    circuit = circuit.copy()
    bit_idx = 0
    while (node := f"x{bit_idx:02}") in circuit:
        circuit[node] = bool((x >> bit_idx) & 1)
        bit_idx += 1

    bit_idx = 0
    while (node := f"y{bit_idx:02}") in circuit:
        circuit[node] = bool((y >> bit_idx) & 1)
        bit_idx += 1

    return circuit


def check_is_adder(circuit: Circuit, num_samples: int = 10) -> bool:
    """
    Iteratively try a random x and y input and verify if the z output is the sum.
    If any check fails, this is not an adder.
    """
    for _ in range(num_samples):
        x = random.getrandbits(45)
        y = random.getrandbits(45)
        circuit = replace_circuit_inputs(circuit, x, y)

        evaluated_nodes: dict[str, bool] = {}
        for bit_idx in range(46):  # Up through 45 so we check the final carryout
            try:
                z_bit = evaluate_node(circuit, f"z{bit_idx:02}", evaluated_nodes)
            except CircuitCycleError:
                return False

            if z_bit != bool(((x + y) >> bit_idx) & 1):
                return False

    return True


def part_1(puzzle_input: str) -> str | int:
    circuit = parse_input(puzzle_input)
    return evaluate_circuit(circuit)


def part_2(puzzle_input: str) -> str | int:
    circuit = parse_input(puzzle_input)

    # Observation: the circuit is a 45-bit ripple carry adder
    # Every output line should (except z45) which is the carryout, should be computed via an XOR
    # In the puzzle input, we see three violations of this: z07, z13, z31
    # We must swap these with intermediate nodes that are XORs of other intermediate nodes
    # There are only 3 such intermediate nodes, and matching these up by hand is straightforward.
    swaps = (("z07", "swt"), ("z13", "pqc"), ("z31", "bgs"))
    for a, b in swaps:
        circuit[a], circuit[b] = circuit[b], circuit[a]

    # Let's just brute-force the rest
    used_nodes = set(itertools.chain.from_iterable(swaps))
    candidate_swaps = {
        node for node in circuit if node not in used_nodes and not node.startswith(("x", "y"))
    }
    for a, b in itertools.combinations(candidate_swaps, 2):
        # Swap
        circuit[a], circuit[b] = circuit[b], circuit[a]

        if check_is_adder(circuit):
            used_nodes.update({a, b})
            return ",".join(sorted(used_nodes))

        # Swap back
        circuit[a], circuit[b] = circuit[b], circuit[a]

    return "Could not find solution"
