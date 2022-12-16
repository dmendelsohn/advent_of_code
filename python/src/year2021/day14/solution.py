from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"


InsertionMap = Dict[Tuple[str, str], str]


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_input(use_test_input: bool = False) -> Tuple[str, InsertionMap]:
    raw_input = read_input(use_test_input)
    lines = raw_input.split("\n")
    return lines[0], {(line[0], line[1]): line[6] for line in lines[2:]}


def apply_rules(seq: List[str], rule_map: InsertionMap) -> List[str]:
    next_seq = []
    for i in range(len(seq) - 1):
        next_seq.append(seq[i])
        insert_char = rule_map.get((seq[i], seq[i + 1]))
        if insert_char:
            next_seq.append(insert_char)
    next_seq.append(seq[-1])
    return next_seq


def get_score(seq: List[str]) -> int:
    most_common = Counter(seq).most_common()
    return most_common[0][1] - most_common[-1][1]


def part_1(use_test_input: bool = False) -> str:
    seq, rule_map = parse_input(use_test_input)
    for i in range(10):
        seq = apply_rules(seq, rule_map)
    score = get_score(seq)
    return f"{score}"


DigramCount = Dict[Tuple[str, str], int]


def get_digram_count(seq: str) -> DigramCount:
    digram_count = defaultdict(int)
    for i in range(len(seq) - 1):
        digram_count[(seq[i], seq[i + 1])] += 1
    return dict(digram_count)


def apply_rules_digram(digram_count: DigramCount, rule_map: InsertionMap) -> DigramCount:
    new_count = defaultdict(int)
    for digram, count in digram_count.items():
        insert_char = rule_map.get(digram)
        if insert_char:
            new_count[(digram[0], insert_char)] += count
            new_count[(insert_char, digram[1])] += count
        else:
            new_count[digram] += count
    return dict(new_count)


def get_monogram_count(
    digram_count: DigramCount, first_char: str, last_char: str
) -> Dict[str, int]:
    double_count = defaultdict(int)
    # Double count everything
    for digram, count in digram_count.items():
        double_count[digram[0]] += count
        double_count[digram[1]] += count
    # Double count start and end
    double_count[first_char] += 1
    double_count[last_char] += 1

    # Back to single counting
    return {char: count // 2 for char, count in double_count.items()}


def part_2(use_test_input: bool = False) -> str:
    start, rules = parse_input(use_test_input)
    first_char, last_char = start[0], start[-1]
    digram_count = get_digram_count(start)
    for i in range(40):
        digram_count = apply_rules_digram(digram_count, rules)
    monogram_count = get_monogram_count(digram_count, first_char, last_char)
    return f"{max(monogram_count.values()) - min(monogram_count.values())}"
