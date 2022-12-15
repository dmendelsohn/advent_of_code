from pathlib import Path
from typing import List, NamedTuple, Tuple

INPUT_PATH = Path(__file__).parent / "input.txt"


class BoardCell(NamedTuple):
    num: int
    is_marked: bool


class Board:
    def __init__(self, cells: List[List[BoardCell]]):
        self.cells = cells

    @classmethod
    def from_input_lines(cls, lines: List[str]) -> "Board":
        cells = []
        for line in lines:
            cell_row = []
            for part in line.strip().split():
                cell_row.append(BoardCell(num=int(part), is_marked=False))
            cells.append(cell_row)
        if len(cells) != 5 or len(cells[0]) != 5:
            raise ValueError(f"OOPS: {cells}")
        return cls(cells)

    def __repr__(self) -> str:
        lines = []
        for row in self.cells:
            line = ""
            for cell in row:
                line += f"{cell.num:02d}"
                if cell.is_marked:
                    line += "(X) "
                else:
                    line += "    "
            lines.append(line)
        return "\n".join(lines)

    def mark_number(self, num: int) -> None:
        for i in range(len(self.cells)):
            for j in range(len(self.cells[0])):
                if self.cells[i][j].num == num:
                    self.cells[i][j] = BoardCell(num=num, is_marked=True)

    def _is_winning_row(self, row_num: int):
        cells = self.cells[row_num]
        return all(cell.is_marked for cell in cells)

    def _is_winning_col(self, col_num: int):
        cells = [row[col_num] for row in self.cells]
        return all(cell.is_marked for cell in cells)

    def is_winner(self) -> bool:
        for row_num in range(len(self.cells)):
            if self._is_winning_row(row_num):
                return True
        for col_num in range(len(self.cells[0])):
            if self._is_winning_col(col_num):
                return True
        return False

    def sum_unmarked(self) -> int:
        count = 0
        for row in self.cells:
            for cell in row:
                if not cell.is_marked:
                    count += cell.num
        return count


def parse_input() -> Tuple[List[int], List[Board]]:
    with open(INPUT_PATH) as f:
        called_nums = [int(elt) for elt in f.readline().strip().split(",")]
        boards = []
        board_buffer = []
        for line in f:
            line = line.strip()
            if line:
                board_buffer.append(line)
            else:
                if board_buffer:
                    boards.append(Board.from_input_lines(board_buffer))
                board_buffer = []
        if board_buffer:
            boards.append(Board.from_input_lines(board_buffer))
    return called_nums, boards


def part_1() -> str:
    called_nums, boards = parse_input()
    for called_num in called_nums:
        for board in boards:
            board.mark_number(called_num)
            if board.is_winner():
                winning_score = board.sum_unmarked()
                print(f"WINNER!\nBoard:\n{board}\nCalled Num:{called_num}\nScore:{winning_score}")
                return f"{winning_score * called_num}"
    return "No winner"


def part_2() -> str:
    called_nums, remaining_boards = parse_input()
    called_num = None
    latest_winner = None
    for called_num in called_nums:
        non_winner_boards = []
        for board in remaining_boards:
            board.mark_number(called_num)
            if board.is_winner():
                latest_winner = board
            if not board.is_winner():
                non_winner_boards.append(board)
        remaining_boards = non_winner_boards
        if not remaining_boards:
            break

    if not latest_winner:
        raise RuntimeError(f"Remaining boards: {remaining_boards}")

    winning_score = latest_winner.sum_unmarked()
    print(f"WINNER!\nBoard:\n{latest_winner}\nCalled Num:{called_num}\nScore:{winning_score}")
    return f"{winning_score * called_num}"
