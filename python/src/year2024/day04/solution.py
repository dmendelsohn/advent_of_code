def is_xmas(
    rows: list[str], start_row: int, start_col: int, row_offset: int, col_offset: int
) -> bool:
    for idx, xmas_chr in enumerate("XMAS"):
        row = start_row + idx * row_offset
        col = start_col + idx * col_offset
        if row < 0 or row >= len(rows) or col < 0 or col >= len(rows[0]):
            return False

        word_chr = rows[row][col]
        if word_chr != xmas_chr:
            return False

    return True


def count_xmas_from_pos(rows: list[str], start_row: int, start_col: int) -> int:
    count = 0
    for row_offset in (-1, 0, 1):
        for col_offset in (-1, 0, 1):
            if row_offset == 0 and col_offset == 0:
                continue
            if is_xmas(rows, start_row, start_col, row_offset, col_offset):
                count += 1
    return count


def count_xmas(rows: list[str]) -> int:
    count = 0
    for row in range(len(rows)):
        for col in range(len(rows[0])):
            count += count_xmas_from_pos(rows, row, col)
    return count


def part_1(puzzle_input: str) -> str | int:
    rows = puzzle_input.split("\n")
    return count_xmas(rows)


def is_cross_mas(rows: list[str], start_row: int, start_col: int) -> bool:
    if start_row < 1 or start_row >= len(rows) - 1:
        return False
    if start_col < 1 or start_col >= len(rows[0]) - 1:
        return False
    if rows[start_row][start_col] != "A":
        return False

    # Corners clockwise from top-left
    corners = "".join(
        [
            rows[start_row + row_offset][start_col + col_offset]
            for (row_offset, col_offset) in ((-1, -1), (-1, 1), (1, 1), (1, -1))
        ]
    )
    return corners in ("MMSS", "SMMS", "SSMM", "MSSM")


def count_cross_mas(rows: list[str]) -> int:
    count = 0
    for row in range(len(rows)):
        for col in range(len(rows[0])):
            count += 1 if is_cross_mas(rows, row, col) else 0
    return count


def part_2(puzzle_input: str) -> str | int:
    rows = puzzle_input.split("\n")
    return count_cross_mas(rows)
