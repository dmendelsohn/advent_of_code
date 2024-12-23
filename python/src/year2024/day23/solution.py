from collections import defaultdict
from typing import DefaultDict


def make_graph(edges: set[frozenset[str]]) -> dict[str, set[str]]:
    graph: DefaultDict[str, set[str]] = defaultdict(set)
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)
    return dict(graph)


def find_cliques(
    prior_cliques: set[frozenset[str]], graph: dict[str, set[str]]
) -> set[frozenset[str]]:
    """Given k-1 cliques, find k-cliques"""
    cliques: set[frozenset[str]] = set()
    for prior_clique in prior_cliques:
        # Select an arbitrary node in prior_clique
        excluded_node = next(iter(prior_clique))
        for included_node in graph[excluded_node]:
            if included_node in prior_clique:
                continue

            if prior_clique.difference({excluded_node}).union({included_node}) in prior_cliques:
                cliques.add(prior_clique.union({included_node}))

    return cliques


def find_max_clique(edges: set[frozenset[str]], graph: dict[str, set[str]]) -> frozenset[str]:
    k_cliques = edges
    while len(k_cliques) > 1:
        k_cliques = find_cliques(k_cliques, graph)

    if len(k_cliques) != 1:
        raise ValueError("Max clique is not unique")

    return k_cliques.pop()


def part_1(puzzle_input: str) -> str | int:
    edges = {frozenset(line.split("-")) for line in puzzle_input.split("\n")}
    graph = make_graph(edges)
    triangles = find_cliques(edges, graph)
    return sum(1 for triangle in triangles if any(node.startswith("t") for node in triangle))


def part_2(puzzle_input: str) -> str | int:
    edges = {frozenset(line.split("-")) for line in puzzle_input.split("\n")}
    graph = make_graph(edges)
    max_clique = find_max_clique(edges, graph)
    return ",".join(sorted(max_clique))
