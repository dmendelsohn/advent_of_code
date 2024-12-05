from collections import defaultdict
from dataclasses import dataclass
from graphlib import TopologicalSorter
from typing import DefaultDict


@dataclass(frozen=True)
class Rule:
    earlier: int
    later: int

    @classmethod
    def from_line(cls, line: str) -> "Rule":
        earlier, later = map(int, line.split("|"))
        return cls(earlier, later)


class Manual(tuple[int]):
    @property
    def middle(self) -> int:
        assert len(self) % 2 == 1
        return self[len(self) // 2]

    @classmethod
    def from_line(cls, line: str) -> "Manual":
        return Manual(map(int, line.split(",")))

    def is_valid(self, rules: set[Rule]) -> bool:
        for i in range(len(self)):
            for j in range(i + 1, len(self)):
                if Rule(self[j], self[i]) in rules:
                    return False
        return True

    def reorder(self, rules: set[Rule]) -> "Manual":
        # Limit to relevant rules
        rules = {rule for rule in rules if rule.earlier in self and rule.later in self}

        # Build a graph
        graph: DefaultDict[int, set[int]] = defaultdict(set)
        for rule in rules:
            graph[rule.earlier].add(rule.later)

        ts = TopologicalSorter(graph)
        return Manual(ts.static_order())


def parse_input(puzzle_input: str) -> tuple[set[Rule], list[Manual]]:
    parts = puzzle_input.split("\n\n")
    assert len(parts) == 2
    rules = {Rule.from_line(line) for line in parts[0].split("\n")}
    manuals = [Manual.from_line(line) for line in parts[1].split("\n")]
    return rules, manuals


def part_1(puzzle_input: str) -> str | int:
    rules, manuals = parse_input(puzzle_input)
    return sum(manual.middle for manual in manuals if manual.is_valid(rules))


def part_2(puzzle_input: str) -> str | int:
    rules, manuals = parse_input(puzzle_input)
    return sum(manual.reorder(rules).middle for manual in manuals if not manual.is_valid(rules))
