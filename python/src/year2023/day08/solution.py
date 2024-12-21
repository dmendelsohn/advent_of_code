import math
import re
from typing import TypeAlias

Graph: TypeAlias = dict[str, tuple[str, str]]


def parse_input(puzzle_input: str) -> tuple[str, Graph]:
    """
    Returns
    - the RL string
    - a mapping of nodes to their left, right children
    """
    instructions, _, *node_lines = puzzle_input.split("\n")
    graph: dict[str, tuple[str, str]] = {}
    for line in node_lines:
        if (match := re.match(r"(\w+) = \((\w+), (\w+)\)", line)) is None:
            raise ValueError(f"Could not parse {line=}")
        parent, left, right = match.groups()
        graph[parent] = (left, right)
    return instructions, graph


def follow_path(instructions: str, graph: Graph) -> int:
    """Follow the instructions to traverse the graph, returning number of steps"""
    num_steps = 0
    node = "AAA"
    while node != "ZZZ":
        inst_idx = num_steps % len(instructions)
        node = graph[node][0] if instructions[inst_idx] == "L" else graph[node][1]
        num_steps += 1
    return num_steps


def get_cycle(instructions: str, graph: Graph, start_node: str) -> tuple[int, int]:
    """Return the cycle start index, the cycle length, and the"""

    # For each (node, instruction idx) track the time we saw it
    last_seen: dict[tuple[str, int], int] = {}
    num_steps = 0
    node = start_node
    while (node, inst_idx := num_steps % len(instructions)) not in last_seen:
        # Record this step
        last_seen[(node, inst_idx)] = num_steps

        # Take the next step
        num_steps += 1
        node = graph[node][0] if instructions[inst_idx] == "L" else graph[node][1]

    cycle_start = last_seen[(node, inst_idx)]
    return cycle_start, num_steps - cycle_start


def find_goal_remainders(
    instructions: str, graph: Graph, start_node: str, cycle_start: int, cycle_length: int
) -> set[int]:
    goal_remainders: set[int] = set()
    num_steps = 0
    node = start_node
    while num_steps < cycle_start + cycle_length:
        if num_steps >= cycle_start and node.endswith("Z"):
            goal_remainders.add(num_steps % cycle_length)

        inst_idx = num_steps % len(instructions)
        node = graph[node][0] if instructions[inst_idx] == "L" else graph[node][1]
        num_steps += 1

    return goal_remainders


def part_1(puzzle_input: str) -> str | int:
    instructions, graph = parse_input(puzzle_input)
    return follow_path(instructions, graph)


def part_2(puzzle_input: str) -> str | int:
    instructions, graph = parse_input(puzzle_input)
    if len(graph) < 10:
        return "Not implemented for example input"

    start_nodes = {node for node in graph if node.endswith("A")}
    lcm = 1
    for node in sorted(start_nodes):
        cycle_start, cycle_length = get_cycle(instructions, graph, node)
        goal_remainders = find_goal_remainders(instructions, graph, node, cycle_start, cycle_length)

        # The input is chosen carefully to have this property, which makes the problem MUCH easier.
        # If there were non-zero goal remainders, and multiple of them, we'd have to do the
        # chinese remainder theorem on every possible combination of remainders.
        assert goal_remainders == {0}

        lcm = math.lcm(lcm, cycle_length)
    return lcm
