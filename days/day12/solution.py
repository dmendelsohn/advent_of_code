from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Set

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"

Graph = Dict[str, Set[str]]
Path = List[str]


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_input(use_test_input: bool = False) -> Graph:
    raw_input = read_input(use_test_input)
    lines = raw_input.split("\n")
    graph = defaultdict(set)
    for line in lines:
        first, second = line.strip().split("-")
        graph[first].add(second)
        graph[second].add(first)
    return dict(graph)


def get_paths_with_no_small_cave_revisits(graph: Graph, path_so_far: Path) -> List[Path]:
    # Note: path must be non-empty
    last_cave = path_so_far[-1]
    if last_cave == "end":
        return [path_so_far.copy()]  # Termination
    elif last_cave.islower() and last_cave in path_so_far[:-1]:
        return []  # Visits short cave twice
    else:
        paths = []
        for next_cave in graph[last_cave]:
            next_path_so_far = path_so_far.copy()
            next_path_so_far.append(next_cave)
            paths.extend(get_paths_with_no_small_cave_revisits(graph, next_path_so_far))
        return paths


def part_1(use_test_input: bool = False) -> str:
    graph = parse_input(use_test_input)
    paths = get_paths_with_no_small_cave_revisits(graph, ["start"])
    return f"{len(paths)}"


def has_multiple_small_cave_revisits(path_so_far: Path) -> bool:
    small_caves = [cave for cave in path_so_far if cave.islower()]
    two_most_common = Counter(small_caves).most_common(2)
    if two_most_common[0][1] > 2:
        # Most common is double-revisited
        return True
    elif len(two_most_common) == 2 and two_most_common[1][1] > 1:
        # Second most common is revisited
        return True
    else:
        return False


def revisits_start(path_so_far: Path) -> bool:
    return path_so_far.count("start") > 1


def get_paths_with_one_small_cave_revisit_allowed(graph: Graph, path_so_far: Path) -> List[Path]:
    # Note: path must be non-empty
    last_cave = path_so_far[-1]
    if last_cave == "end":
        return [path_so_far.copy()]  # Termination
    elif has_multiple_small_cave_revisits(path_so_far) or revisits_start(path_so_far):
        return []
    else:
        paths = []
        for next_cave in graph[last_cave]:
            next_path_so_far = path_so_far.copy()
            next_path_so_far.append(next_cave)
            paths.extend(get_paths_with_one_small_cave_revisit_allowed(graph, next_path_so_far))
        return paths


def part_2(use_test_input: bool = False) -> str:
    graph = parse_input(use_test_input)
    paths = get_paths_with_one_small_cave_revisit_allowed(graph, ["start"])
    return f"{len(paths)}"
