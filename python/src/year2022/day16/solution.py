import re
from functools import cache
from typing import FrozenSet

Valves = set[str]
Flows = dict[str, int]
Weights = dict[tuple[str, str], int]
Graph = tuple[Valves, Flows, Weights]


def get_raw_graph(text: str) -> Graph:
    valves = set()
    flows = {}
    weights = {}
    reg = r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)"
    for valve, flow, neighbors in re.findall(reg, text):
        valves.add(valve)
        if flow != "0":
            flows[valve] = int(flow)
        for neighbor in neighbors.split(", "):
            weights[(valve, neighbor)] = 1

    return valves, flows, weights


def densify_graph(graph: Graph) -> None:
    # Add weights representing the pairwise-shortest paths between all nodes
    valves, flows, weights = graph
    for k in valves:
        for i in valves:
            for j in valves:
                weights[i, j] = min(
                    weights.get((i, j), 1000),
                    weights.get((i, k), 1000) + weights.get((k, j), 1000),
                )


def make_get_max_flow(
    graph: Graph,
):
    valves, flows, weights = graph

    @cache
    def _get_max_flow(
        time_remaining: int,
        start: str,
        closed_valves: FrozenSet[str],
        helper_time_remaining: int = 0,
    ):
        max_flow = 0
        for next_valve in closed_valves:
            if weights[start, next_valve] + 1 < time_remaining:
                next_time_remaining = time_remaining - weights[start, next_valve] - 1
                flow = flows[next_valve] * next_time_remaining + _get_max_flow(
                    next_time_remaining,
                    next_valve,
                    closed_valves - {next_valve},
                    helper_time_remaining,
                )
                max_flow = max(max_flow, flow)

        # Alternatively, rely on the helper only
        if helper_time_remaining > 0:
            helper_flow = _get_max_flow(
                helper_time_remaining,
                "AA",
                closed_valves,
                0,
            )
            max_flow = max(max_flow, helper_flow)

        return max_flow

    return _get_max_flow


get_max_flow = None


def part_1(puzzle_input: str) -> str | int:
    graph = get_raw_graph(puzzle_input)
    densify_graph(graph)

    global get_max_flow
    if get_max_flow is None:
        get_max_flow = make_get_max_flow(graph)

    useful_valves = frozenset(graph[1].keys())
    return get_max_flow(30, "AA", useful_valves)


def part_2(puzzle_input: str) -> str | int:
    graph = get_raw_graph(puzzle_input)
    densify_graph(graph)

    global get_max_flow
    if get_max_flow is None:
        get_max_flow = make_get_max_flow(graph)

    useful_valves = frozenset(graph[1].keys())
    return get_max_flow(26, "AA", useful_valves, 26)
