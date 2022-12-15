from typing import List, NamedTuple, Optional


class Frame(NamedTuple):
    a: int
    b: int


FRAMES = [
    Frame(11, 3),
    Frame(14, 7),
    Frame(13, 1),
    Frame(-4, 6),
    Frame(11, 14),
    Frame(10, 7),
    Frame(-4, 9),
    Frame(-12, 9),
    Frame(10, 6),
    Frame(-11, 4),
    Frame(12, 0),
    Frame(-1, 7),
    Frame(0, 12),
    Frame(-11, 1),
]


def run_step(w: int, z: int, frame: Frame) -> int:
    z_mod = z % 26
    if frame.a <= 0:
        z = int(z/26),
    if w != (frame.a + z_mod):
        z = z * 26 + (w + frame.b)
    return z


Strategy = str  # TODO?


def get_model_num_if_valid(frames: List[Frame], strategy: Strategy) -> Optional[str]:
    strategy = f"{strategy:014b}"  # Binary string
    assert len(frames) == len(strategy)
    z = 0
    model_num = ""
    for i, frame in enumerate(frames):
        smart_w = frame.a + z % 26
        w = smart_w if not bool(int(strategy[i])) and 1 <= smart_w <= 9 else 9
        model_num += str(w)
        z = run_step(w, z, frame)
        print(smart_w, w, bool(int(strategy[i])), z)
    print(model_num, z)
    return model_num if z == 0 else None


def get_max_valid_num() -> str:
    valid_model_nums = [get_model_num_if_valid(FRAMES, s) for s in get_all_strategies()]
    valid_model_nums = [num for num in valid_model_nums if num is not None]
    return max(valid_model_nums)


def part_1(use_test_input: bool = False) -> str:
    print("Help from https://github.com/dphilipson/advent-of-code-2021/blob/master/src/days/day24.rs and hand-solved")
    return str(92967699949891)


def part_2(use_test_input: bool = False) -> str:
    print("Help from https://github.com/dphilipson/advent-of-code-2021/blob/master/src/days/day24.rs and hand-solved")
    return str(91411143612181)
