import functools
import itertools

Packet = list[list | int]


def parse_input(text: str) -> list[tuple[Packet, Packet]]:
    packet_pairs = []
    for line_pair in text.split("\n\n"):
        first_line, second_line = line_pair.split("\n")
        packet_pairs.append((eval(first_line), eval(second_line)))
    return packet_pairs


def compare(first, second) -> int:
    """Returns -1 if first < second, 0 if first == second, 1 if first > second"""
    idx = 0
    while idx < min(len(first), len(second)):
        first_elt, second_elt = first[idx], second[idx]
        idx += 1
        if isinstance(first_elt, int) and isinstance(second_elt, int):
            if first_elt < second_elt:
                return -1
            elif first_elt > second_elt:
                return 1
        elif isinstance(first_elt, list) and isinstance(second_elt, list):
            if (sub_compare := compare(first_elt, second_elt)) != 0:
                return sub_compare
        elif isinstance(first_elt, int) and isinstance(second_elt, list):
            if sub_compare := compare([first_elt], second_elt):
                return sub_compare
        else:
            if sub_compare := compare(first_elt, [second_elt]):
                return sub_compare

    # Got to end with no differences, use length as tiebreaker
    if len(first) < len(second):
        return -1
    elif len(first) > len(second):
        return 1

    # Packets are identical
    return 0


def part_1(puzzle_input: str) -> str | int:
    pairs = parse_input(puzzle_input)
    return sum((idx + 1) for idx, pair in enumerate(pairs) if compare(*pair) < 0)


def part_2(puzzle_input: str) -> str | int:
    divider_packets = [[[2]], [[6]]]
    packets: list = sorted(
        list(itertools.chain(*parse_input(puzzle_input))) + divider_packets,
        key=functools.cmp_to_key(compare),
    )
    return (1 + packets.index(divider_packets[0])) * (1 + packets.index(divider_packets[1]))
