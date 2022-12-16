from pathlib import Path
from typing import Dict, FrozenSet, List, NamedTuple, Set, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"

DigitSignal = FrozenSet[str]  # Subset of set("abcdefg")


class Entry(NamedTuple):
    digit_signals: Set[DigitSignal]  # 10 unique signals corresponding to "0" through "9" displays
    output_signals: List[DigitSignal]  # 4 output signals

    @classmethod
    def from_line(cls, line: str) -> "Entry":
        digit_signals_str, output_signals_str = line.strip().split(" | ")
        digit_signals = {
            frozenset(signal_str) for signal_str in digit_signals_str.strip().split(" ")
        }
        output_signals = [
            frozenset(signal_str) for signal_str in output_signals_str.strip().split(" ")
        ]
        return Entry(digit_signals=digit_signals, output_signals=output_signals)


def deduce_digit(
    known_digits: Dict[str, DigitSignal], signals: Set[DigitSignal]
) -> Tuple[str, DigitSignal]:
    for signal in signals:
        unique_count_signals = {2: "1", 3: "7", 4: "4", 7: "8"}
        if len(signal) in unique_count_signals:
            return unique_count_signals[len(signal)], signal

        elif len(signal) == 5:
            if "9" in known_digits and not signal < known_digits["9"]:
                # 2 is only 5-segment signal that is not a subset of 9
                return "2", signal
            elif "1" in known_digits and signal > known_digits["1"]:
                # 3 is only 5-segment signal that is superset of 1
                return "3", signal
            elif "6" in known_digits and signal < known_digits["6"]:
                # 5 is only 5-segment signal that is a subset of 6
                return "5", signal

        elif len(signal) == 6:  # Pick between 0, 6, 9
            if (
                "1" in known_digits
                and signal > known_digits["1"]
                and "4" in known_digits
                and not signal > known_digits["4"]
            ):
                # 0 is only 6-segment signal that is superset of 1 but not 4
                return "0", signal
            elif "1" in known_digits and not signal > known_digits["1"]:
                # 6 is only 6-segment signal that is not superset of 1
                return "6", signal
            elif "4" in known_digits and signal > known_digits["4"]:
                # 9 is only 6-segment signal that is superset of 4
                return "9", signal

    raise RuntimeError(f"Could not find a digit in {signals} given {known_digits}")


def deduce_digits(digit_signals: Set[DigitSignal]) -> Dict[str, DigitSignal]:
    known_digits = dict()
    remaining_signals = digit_signals.copy()
    while remaining_signals:
        digit, signal = deduce_digit(known_digits, remaining_signals)
        known_digits[digit] = signal
        remaining_signals.remove(signal)

    return known_digits


def decode(entry: Entry) -> int:
    digits = deduce_digits(entry.digit_signals)
    signal_to_digit = {v: k for k, v in digits.items()}
    output_digits = [signal_to_digit[signal] for signal in entry.output_signals]
    return int("".join(output_digits))


def parse_input(use_test_input: bool = False) -> List[Entry]:
    input_path = TEST_INPUT_PATH if use_test_input else INPUT_PATH
    return [Entry.from_line(line) for line in open(input_path).read().strip().split("\n")]


def part_1(use_test_input: bool = False) -> str:
    entries = parse_input(use_test_input)
    num_simple_digits = 0
    for entry in entries:
        for output_signal in entry.output_signals:
            if len(output_signal) in (2, 3, 4, 7):
                num_simple_digits += 1
    return f"{num_simple_digits}"


def part_2(use_test_input: bool = False) -> str:
    entries = parse_input(use_test_input)
    total = 0
    for entry in entries:
        total += decode(entry)
    return f"{total}"
