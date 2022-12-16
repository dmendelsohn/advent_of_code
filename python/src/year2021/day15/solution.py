from functools import total_ordering
from pathlib import Path
from queue import PriorityQueue
from typing import Dict, List, NamedTuple, Optional, Set

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"


class Point(NamedTuple):
    x: int
    y: int

    def neighbors(self) -> Set["Point"]:
        return {
            Point(self.x + 1, self.y),
            Point(self.x - 1, self.y),
            Point(self.x, self.y + 1),
            Point(self.x, self.y - 1),
        }


@total_ordering
class WeightedPath(NamedTuple):
    points: List[Point]
    weight: int  # Could be derived from path and graph, but nice to not recalculate every time

    def add(self, point: Point, weight: int) -> "WeightedPath":
        return WeightedPath(self.points[:] + [point], self.weight + weight)

    def __lt__(self, other: "WeightedPath") -> bool:
        return self.weight < other.weight


Graph = Dict[Point, int]


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_input(use_test_input: bool = False) -> Graph:
    point_weights = dict()
    x = y = 0
    for char in read_input(use_test_input):
        if char == "\n":
            y += 1
            x = 0
        else:
            point_weights[Point(x, y)] = int(char)
            x += 1
    return point_weights


def find_shortest_path(graph: Graph) -> Optional[WeightedPath]:
    """Implementation of Dijkstra's algorithm"""
    # Initialize things
    start = Point(0, 0)
    dest = max(graph.keys())
    tentative_paths = {
        point: WeightedPath([start], 0) if point == start else None for point in graph.keys()
    }
    unvisited_points = set(graph.keys())

    path_queue = PriorityQueue()
    path_queue.put(tentative_paths[start])

    # Loop until we find the exit
    current_point = start
    while True:
        if current_point == dest:
            break

        path_to_current_point = tentative_paths[current_point]
        for neighbor in current_point.neighbors():
            if neighbor in graph and neighbor in unvisited_points:
                proposed_path_to_neighbor = path_to_current_point.add(
                    point=neighbor, weight=graph[neighbor]
                )
                existing_path_to_neighbor = tentative_paths.get(neighbor)
                if (
                    not existing_path_to_neighbor
                    or proposed_path_to_neighbor.weight < existing_path_to_neighbor.weight
                ):
                    tentative_paths[neighbor] = proposed_path_to_neighbor
                    path_queue.put(proposed_path_to_neighbor)

        # Mark as visited
        unvisited_points.remove(current_point)

        # Pick next unvisited point off the queue
        next_path = path_queue.get()
        current_point = next_path.points[-1]
        while current_point not in unvisited_points:
            next_path = path_queue.get()
            current_point = next_path.points[-1]

    return tentative_paths[dest]


def part_1(use_test_input: bool = False) -> str:
    graph = parse_input(use_test_input)
    path = find_shortest_path(graph=graph)
    if path:
        print(path)
        return f"{path.weight}"
    else:
        return "No path found"


def extend_graph(graph: Graph) -> Graph:
    # Use input graph as 5x5 tiling
    output = dict()
    bottom_right = max(graph.keys())
    xdim, ydim = bottom_right.x + 1, bottom_right.y + 1
    for xcount in range(5):
        for ycount in range(5):
            for original_point, original_weight in graph.items():
                point = Point(original_point.x + xcount * xdim, original_point.y + ycount * ydim)
                weight = ((original_weight + xcount + ycount) - 1) % 9 + 1
                output[point] = weight
    return output


def print_graph(graph: Graph) -> None:
    char_buffer = []
    bottom_right = max(graph.keys())
    for y in range(bottom_right.y + 1):
        for x in range(bottom_right.x + 1):
            char_buffer.append(str(graph[Point(x, y)]))
        char_buffer.append("\n")
    print("".join(char_buffer))


def part_2(use_test_input: bool = False) -> str:
    graph = parse_input(use_test_input)
    graph = extend_graph(graph)
    path = find_shortest_path(graph=graph)
    if path:
        print(path)
        return f"{path.weight}"
    else:
        return "No path found"
