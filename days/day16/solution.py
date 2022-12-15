from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"


Bitstream = List[bool]


class Packet(ABC):

    def __init__(self, *, version: int, type_id: int):
        self.version = version
        self.type_id = type_id

    @abstractmethod
    def eval(self) -> int:
        pass

    @abstractmethod
    def version_sum(self) -> int:
        pass


class LiteralPacket(Packet):

    def __init__(self, *, value: int, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def eval(self) -> int:
        return self.value

    def version_sum(self) -> int:
        return self.version

    def __str__(self) -> str:
        return f"{self.value}"


class OperatorPacket(Packet):

    def __init__(self, *, operands: List[Packet], **kwargs):
        super().__init__(**kwargs)
        if not operands:
            raise ValueError("Cannot have zero operands")
        self.operands = operands

    def eval(self) -> int:
        if self.type_id == 0:
            return sum(operand.eval() for operand in self.operands)
        elif self.type_id == 1:
            product = 1
            for operand in self.operands:
                product *= operand.eval()
            return product
        elif self.type_id == 2:
            return min(operand.eval() for operand in self.operands)
        elif self.type_id == 3:
            return max(operand.eval() for operand in self.operands)
        elif self.type_id == 5:
            if len(self.operands) != 2:
                raise ValueError(f"Cannot do operator {self.type_id} on {len(self.operands)} inputs")
            return 1 if self.operands[0].eval() > self.operands[1].eval() else 0
        elif self.type_id == 6:
            if len(self.operands) != 2:
                raise ValueError(f"Cannot do operator {self.type_id} on {len(self.operands)} inputs")
            return 1 if self.operands[0].eval() < self.operands[1].eval() else 0
        elif self.type_id == 7:
            if len(self.operands) != 2:
                raise ValueError(f"Cannot do operator {self.type_id} on {len(self.operands)} inputs")
            return 1 if self.operands[0].eval() == self.operands[1].eval() else 0
        else:
            raise ValueError(f"Unknown operator type_id = {self.type_id}")

    def version_sum(self) -> int:
        return self.version + sum(operand.version_sum() for operand in self.operands)

    def __str__(self) -> str:
        op_str = {
            0: "ADD",
            1: "MUL",
            2: "MIN",
            3: "MAX",
            5: "GT",
            6: "LT",
            7: "EQ",
        }[self.type_id]
        return f"{op_str}({', '.join(str(operand) for operand in self.operands)})"


def bitstream_to_str(bitstream: Bitstream) -> str:
    return "".join(str(int(bit)) for bit in bitstream)


def parse_int(bitstream: Bitstream, num_bits: int) -> Tuple[int, Bitstream]:
    try:
        return int(bitstream_to_str(bitstream[:num_bits]), 2), bitstream[num_bits:]
    except ValueError:
        raise ValueError(f"Could not parse {num_bits} bit from '{bitstream_to_str(bitstream)}'")


def parse_literal(bitstream: Bitstream) -> Tuple[int, Bitstream]:
    literal_bits = []
    while True:
        header_bit, value_bits, bitstream = bitstream[0], bitstream[1:5], bitstream[5:]
        literal_bits.extend(value_bits)
        if not header_bit:
            break
    return int(bitstream_to_str(literal_bits), 2), bitstream


def parse_packet(bitstream: Bitstream) -> Tuple[Packet, Bitstream]:
    version, bitstream = parse_int(bitstream, 3)
    type_id, bitstream = parse_int(bitstream, 3)
    if type_id == 4:
        value, bitstream = parse_literal(bitstream)
        return LiteralPacket(version=version, type_id=type_id, value=value), bitstream
    else:
        length_type_id, bitstream = parse_int(bitstream, 1)
        if length_type_id:
            length_in_packets, bitstream = parse_int(bitstream, 11)
            operands = []
            for _ in range(length_in_packets):
                operand, bitstream = parse_packet(bitstream)
                operands.append(operand)
        else:
            length_in_bits, bitstream = parse_int(bitstream, 15)
            operands_bitstream, bitstream = bitstream[:length_in_bits], bitstream[length_in_bits:]
            operands = []
            while operands_bitstream:
                operand, operands_bitstream = parse_packet(operands_bitstream)
                operands.append(operand)

        return OperatorPacket(version=version, type_id=type_id, operands=operands), bitstream


def read_input(use_test_input: bool = False) -> str:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return open(input_path).read().strip()


def parse_input(use_test_input: bool = False) -> Bitstream:
    hex_str = read_input(use_test_input)
    bitstream = []
    for hex_char in hex_str:
        binary_str = bin(int(hex_char, 16))[2:].zfill(4)
        for binary_char in binary_str:
            bitstream.append(bool(int(binary_char)))
    return bitstream


def part_1(use_test_input: bool = False) -> str:
    bitstream = parse_input(use_test_input)
    packet, bitstream = parse_packet(bitstream)
    if any(bit for bit in bitstream):
        raise RuntimeError(f"Bitstream has non-empty remainder: {bitstream_to_str(bitstream)}")
    return f"{packet.version_sum()}"


def part_2(use_test_input: bool = False) -> str:
    # Attempt 1: 49067 is too low
    # Answer 2: 834151779165 is correct
    bitstream = parse_input(use_test_input)
    packet, bitstream = parse_packet(bitstream)
    if any(bit for bit in bitstream):
        raise RuntimeError(f"Bitstream has non-empty remainder: {bitstream_to_str(bitstream)}")
    return f"{packet.eval()}"
