import re
import itertools
from typing import Iterable


def validate_str(string: str) -> bool:
    """ Validate a string as a representation of Sudoku
    DOES NOT check whether if it is a valid answer in Sudoku

    Return False for empty input
    >>> validate_str('')
    False

    Return True for any combination of . and 1-9 with length 81
    >>> validate_str('..9..5.1.85.4....2432......1...69.83.9.....6.62.71...9......1945....4.37.4.3..6..')
    True

    Return False if length is not exactly 81
    >>> validate_str('..9..5.1.85.4....2432......1...69.83.9.....6.62.71...9......1945....4.37.4.3..6..1')
    False

    Return False if any of the char are not . or 1-9
    >>> validate_str('A.9..5.1.85.4...2432......1...69.83.9.....6.62.71...9......1945....4.37.4.3..6..1')
    False
    """
    return bool(re.match(r"^[0-9\.]{81}$", string))


def row(n: int) -> Iterable[int]:
    """ return an iterable with indice of cells that belongs to row n
    >>> list(row(1))
    [0, 1, 2, 3, 4, 5, 6, 7, 8]
    >>> list(row(2))
    [9, 10, 11, 12, 13, 14, 15, 16, 17]
    >>> list(row(9))
    [72, 73, 74, 75, 76, 77, 78, 79, 80]
    """
    return range((n - 1) * 9, n * 9)


def square(n: int) -> Iterable[int]:
    """ return an iterable with indice of cells that belongs to square n
    >>> list(square(1))
    [0, 1, 2, 9, 10, 11, 18, 19, 20]
    >>> list(square(4))
    [27, 28, 29, 36, 37, 38, 45, 46, 47]
    >>> list(square(9))
    [60, 61, 62, 69, 70, 71, 78, 79, 80]
    """
    row_offset = ((n - 1) // 3) * 27
    column_offset = ((n - 1) % 3) * 3
    start = row_offset + column_offset
    return itertools.chain(range(start, start+3), range(start+9, start+12), range(start+18, start+21))


def column(n: int) -> Iterable[int]:
    """ return an iterable with indice of cells that belongs to column n
    >>> list(column(1))
    [0, 9, 18, 27, 36, 45, 54, 63, 72]
    >>> list(column(9))
    [8, 17, 26, 35, 44, 53, 62, 71, 80]
    """
    return range((n-1), 81, 9)


def cell_to_row(idx: int) -> int:
    """ return the row number of a cell
    >>> cell_to_row(0)
    1

    >>> cell_to_row(35)
    4

    >>> cell_to_row(75)
    9
    """
    return idx // 9 + 1


def cell_to_column(idx: int) -> int:
    """ return the column number of a cell
    >>> cell_to_column(0)
    1

    >>> cell_to_column(24)
    7

    >>> cell_to_column(49)
    5

    >>> cell_to_column(74)
    3
    """
    return idx % 9 + 1


def cell_to_square(idx: int) -> int:
    """ return the square number of a cell
    >>> cell_to_square(0)
    1

    >>> cell_to_square(24)
    3

    >>> cell_to_square(49)
    5

    >>> cell_to_square(74)
    7
    """
    x_offset = (idx % 9) // 3 + 1
    y_offset = (idx // 27) * 3
    return x_offset + y_offset


def same_row_column_square(idx: int) -> list[int]:
    """ return an iterable of cells in same row/column/square.
    >>> set(same_row_column_square(0))
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 27, 36, 45, 54, 63, 72}

    >>> set(same_row_column_square(51))
    {6, 15, 24, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 60, 69, 78}
    """
    r = cell_to_row(idx)
    c = cell_to_column(idx)
    s = cell_to_square(idx)
    return itertools.chain(row(r), column(c), square(s))


BitTable = {}


def count_bit(num: int) -> int:
    """ util function to count the 1 bits in a binary number
    >>> count_bit(0)
    0

    >>> count_bit(1)
    1

    >>> count_bit(8)
    1

    >>> count_bit(3)
    2

    >>> count_bit(500)
    6
    """
    if num in BitTable:
        return BitTable[num]
    else:
        count = 0
        bit = num
        while bit != 0:
            count += 1
            bit = bit & (bit - 1)
        BitTable[num] = count
        return count


def update_candidates(candidates: list[int], idx: int, number: int) -> list[int]:
    """
    update a list representation of number candidates in a sudoku.
    valid numbers are represented by bits.
    e.g.: 
    0: all nums in 1-9 are valid
    3: ( = 0b000000011) num 1 & 2 are not valid
    511: (= 0b111111111) all nums in 1-9 are not valid
    >>> update_candidates([0 for _ in range(81)], 0, 3)
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 
     4, 4, 4, 0, 0, 0, 0, 0, 0,
     4, 4, 4, 0, 0, 0, 0, 0, 0,
     4, 0, 0, 0, 0, 0, 0, 0, 0, 
     4, 0, 0, ... 0]
    """
    new_candidates = candidates.copy()
    for idx in same_row_column_square(idx):
        new_candidates[idx] |= (1 << (number - 1))
    return new_candidates


def solve(sudoku: str):
    if not validate_str(sudoku):
        raise ValueError('cannot interpret this sudoku string')

    sudoku = sudoku.replace('.', '0')
    candidates = [0 for _ in range(81)]
    for idx in range(81):
        if sudoku[idx] != '0':
            candidates = update_candidates(candidates, idx, sudoku[idx])


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS |
                    doctest.NORMALIZE_WHITESPACE)
