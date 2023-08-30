from enum import Enum
from typing import FrozenSet, Iterator

# A set of filled spots relative to the bottom-left of bounding box
# tuple items are (row_offset, col_offset)
Piece = FrozenSet[tuple[int, int]]

# List of rows (starting from bottom, going to top non-empty row)
# Rows are lists of cells (left-to-right)
# The grid only includes "locked-in" pieces, not the actively falling one
Grid = list[list[bool]]

GRID_WIDTH = 7


class Gust(Enum):
    LEFT = "<"
    RIGHT = ">"


PIECES = [
    frozenset({(0, 0), (0, 1), (0, 2), (0, 3)}),
    frozenset({(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)}),
    frozenset({(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)}),
    frozenset({(0, 0), (1, 0), (2, 0), (3, 0)}),
    frozenset({(0, 0), (1, 0), (0, 1), (1, 1)}),
]


class GustsIterator(Iterator):
    def __init__(self, puzzle_input: str):
        self.gusts = [Gust(char) for char in puzzle_input]
        self.index = 0

    def __next__(self) -> Gust:
        ret = self.gusts[self.index]
        self.index = (self.index + 1) % len(self.gusts)
        return ret


def can_fit(grid: Grid, piece: Piece, row: int, col: int) -> bool:
    """Returns whether a piece could fit in the grid at a specified location"""
    for row_offset, col_offset in piece:
        cell_row, cell_col = row + row_offset, col + col_offset
        if cell_col < 0 or cell_col >= GRID_WIDTH or cell_row < 0:
            # Hits wall or floor
            return False
        if cell_row < len(grid) and grid[cell_row][cell_col]:
            # Cell is occupied
            return False
    return True


def lock_piece(grid: Grid, piece: Piece, row: int, col: int) -> None:
    """Places the given piece in the grid (does not check for whether it is already occupied)"""
    for row_offset, col_offset in piece:
        cell_row, cell_col = row + row_offset, col + col_offset
        # Add new rows to grid as needed
        while cell_row >= len(grid):
            grid.append([False] * GRID_WIDTH)
        grid[cell_row][cell_col] = True


def drop_piece(grid: Grid, piece: Piece, gusts: Iterator[Gust]) -> None:
    """Executes the fall and placement of a single piece into the grid"""
    row, col = len(grid) + 3, 2
    while True:
        gust = next(gusts)
        if gust == Gust.LEFT and can_fit(grid, piece, row, col - 1):
            col -= 1
        elif gust == Gust.RIGHT and can_fit(grid, piece, row, col + 1):
            col += 1

        if can_fit(grid, piece, row - 1, col):
            row -= 1
        else:
            break

    lock_piece(grid, piece, row, col)


def part_1(puzzle_input: str) -> str | int:
    grid: Grid = []
    piece_idx = 0
    gusts = GustsIterator(puzzle_input)
    for _ in range(2022):
        drop_piece(grid, PIECES[piece_idx], gusts)
        piece_idx = (piece_idx + 1) % len(PIECES)
    return len(grid)


def get_cycle(grid: Grid, gusts: GustsIterator) -> tuple[int, int, int]:
    """
    Drop full 5-piece sets until we hit the same place in GustsIterator
    Elements of return tuple
    - number of pieces dropped total
    - number of pieces in a cycle
    - height added by a cycle
    """
    # Seen maps gust indices to (num pieces dropped, height)
    seen: dict[int, tuple[int, int]] = {}
    num_pieces_dropped = 0
    while gusts.index not in seen:
        seen[gusts.index] = (num_pieces_dropped, len(grid))

        # Drop a full set of pieces
        for idx in range(len(PIECES)):
            drop_piece(grid, PIECES[idx], gusts)
            num_pieces_dropped += 1

    cycle_start_num_pieces, cycle_start_height = seen[gusts.index]
    return (
        num_pieces_dropped,
        num_pieces_dropped - cycle_start_num_pieces,
        len(grid) - cycle_start_height,
    )


def part_2(puzzle_input: str) -> str | int:
    total_drops = 10**12
    grid: Grid = []
    gusts = GustsIterator(puzzle_input)
    num_pieces_dropped = 0

    # See the grid with 100 sets of pieces, to hit a stable cycle
    for _ in range(100):
        for piece_idx in range(len(PIECES)):
            drop_piece(grid, PIECES[piece_idx], gusts)
            num_pieces_dropped += 1

    res = get_cycle(grid, gusts)
    num_pieces_dropped += res[0]
    cycle_num_pieces = res[1]
    cycle_added_height = res[2]

    # Iterate until we are an integer number of cycles from the end
    piece_idx = 0
    while (total_drops - num_pieces_dropped) % cycle_num_pieces != 0:
        drop_piece(grid, PIECES[piece_idx], gusts)
        piece_idx = (piece_idx + 1) % len(PIECES)
        num_pieces_dropped += 1

    remaining_cycles = (total_drops - num_pieces_dropped) // cycle_num_pieces
    remaining_height = remaining_cycles * cycle_added_height
    return len(grid) + remaining_height
