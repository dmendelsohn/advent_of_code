from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, NamedTuple, Optional, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"
TEST_INPUT_PATH = Path(__file__).parent / "test_input.txt"


def get_starting_points(use_test_input: bool) -> Tuple[int, int]:
    if use_test_input:
        return 4, 8
    else:
        return 1, 2


class Die(ABC):
    @abstractmethod
    def roll(self) -> int:
        pass


class DeterministicDie(Die):
    def __init__(self, num_sides: int):
        self.num_sides = num_sides
        self.next_roll = 1

    def roll(self) -> int:
        result = self.next_roll
        self.next_roll = self.next_roll % self.num_sides + 1
        return result


class Game:
    def __init__(self, p1_pos: int, p2_pos: int, die: Die):
        self.p1_pos = p1_pos
        self.p2_pos = p2_pos
        self.die = die
        self.p1_score = self.p2_score = 0
        self.num_turns = 0

    def play_turn(self) -> None:
        self.num_turns += 1
        roll_total = sum([self.die.roll(), self.die.roll(), self.die.roll()])
        if self.num_turns % 2:
            self.p1_pos = (self.p1_pos + roll_total - 1) % 10 + 1
            self.p1_score += self.p1_pos
        else:
            self.p2_pos = (self.p2_pos + roll_total - 1) % 10 + 1
            self.p2_score += self.p2_pos


def part_1(use_test_input: bool = False) -> str:
    p1_pos, p2_pos = get_starting_points(use_test_input)
    die = DeterministicDie(100)
    game = Game(p1_pos, p2_pos, die)
    while max(game.p1_score, game.p2_score) < 1000:
        game.play_turn()
    losing_score = min(game.p1_score, game.p2_score)
    num_rolls = 3 * game.num_turns
    print(f"Losing score = {losing_score}")
    print(f"Num rolls = {num_rolls}")
    return f"{losing_score * num_rolls}"


class PlayerState(NamedTuple):
    pos: int
    points_to_win: int


class GameState(NamedTuple):
    on_player_state: PlayerState
    off_player_state: PlayerState

    def next_state(self, roll_total: int) -> "GameState":
        next_pos = (self.on_player_state.pos + roll_total - 1) % 10 + 1
        next_ptw = max(self.on_player_state.points_to_win - next_pos, 0)
        return GameState(self.off_player_state, PlayerState(pos=next_pos, points_to_win=next_ptw))


class GameResult(NamedTuple):
    on_player_wins: int
    off_player_wins: int

    def __add__(self, other: "GameResult") -> "GameResult":
        return GameResult(self.on_player_wins + other.on_player_wins, self.off_player_wins + other.off_player_wins)

    def __mul__(self, other: int) -> "GameResult":
        return GameResult(other * self.on_player_wins, other * self.off_player_wins)

    @property
    def inverse(self) -> "GameResult":
        return GameResult(self.off_player_wins, self.on_player_wins)


ROLL_WAYS = {
    3: 1,  # 111
    4: 3,  # 112, 121, 211
    5: 6,  # 113, 122, 131, 212, 221, 311
    6: 7,  # 123, 132, 213, 222, 231, 312, 321
    7: 6,  # 133, 223, 232, 313, 322, 331
    8: 3,  # 233, 323, 332
    9: 1,  # 333
}


def get_game_result(game_state: GameState, memo: Dict[GameState, GameResult]) -> GameResult:
    if game_state in memo:
        return memo[game_state]

    if game_state.off_player_state.points_to_win <= 0:
        # Last player won on their turn
        result = GameResult(on_player_wins=0, off_player_wins=1)
    else:
        # Game isn't over, recurse over possible turn outcomes and accumulate them
        result = GameResult(0, 0)
        for roll_total, num_ways in ROLL_WAYS.items():
            next_game_state = game_state.next_state(roll_total)
            next_game_result = get_game_result(next_game_state, memo).inverse
            result += next_game_result * num_ways

    memo[game_state] = result
    return result


def part_2(use_test_input: bool = False) -> str:
    p1_pos, p2_pos = get_starting_points(use_test_input)
    target = 21
    game_state = GameState(PlayerState(pos=p1_pos, points_to_win=target), PlayerState(pos=p2_pos, points_to_win=target))
    memo = dict()
    game_result = get_game_result(game_state, memo)
    print(f"Game result: {game_result}")
    return f"{max((game_result.on_player_wins, game_result.off_player_wins))}"