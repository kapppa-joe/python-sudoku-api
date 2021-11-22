import re
import itertools
from typing import Iterable
from utils import count_bit


class Sudoku():
    def __init__(self, width=3):
        """ return a new sudoku instance.
            width denotes the width of a square
            default to be the common 3x3 sudoku.
        >>> s = Sudoku()
        >>> s.width
        3
        >>> s.max_num
        9
        >>> s2 = Sudoku(2)
        >>> s2.width
        2
        >>> s2.max_num
        4
        """
        self.width = width
        self.max_num = width ** 2
        self.number_of_cells = width ** 4

    # def validate_str(string: str) -> bool:
    #     """ Validate a string as a representation of Sudoku
    #     DOES NOT check whether if it is a valid answer in Sudoku

    #     Return False for empty input
    #     >>> validate_str('')
    #     False

    #     Return True for any combination of . and 1-9 with length 81
    #     >>> validate_str('..9..5.1.85.4....2432......1...69.83.9.....6.62.71...9......1945....4.37.4.3..6..')
    #     True

    #     Return False if length is not exactly 81
    #     >>> validate_str('..9..5.1.85.4....2432......1...69.83.9.....6.62.71...9......1945....4.37.4.3..6..1')
    #     False

    #     Return False if any of the char are not . or 1-9
    #     >>> validate_str('A.9..5.1.85.4...2432......1...69.83.9.....6.62.71...9......1945....4.37.4.3..6..1')
    #     False
    #     """
    #     return bool(re.match(r"^[0-9\.]{81}$", string))

    def row(self, n: int) -> Iterable[int]:
        """ return an iterable with indice of cells that belongs to row n
        >>> sudoku = Sudoku()
        >>> list(sudoku.row(1))
        [0, 1, 2, 3, 4, 5, 6, 7, 8]
        >>> list(sudoku.row(2))
        [9, 10, 11, 12, 13, 14, 15, 16, 17]
        >>> list(sudoku.row(9))
        [72, 73, 74, 75, 76, 77, 78, 79, 80]

        >>> sudoku2x2 = Sudoku(width=2)
        >>> list(sudoku2x2.row(1))
        [0, 1, 2, 3]
        """
        return range((n - 1) * self.max_num, n * self.max_num)

    def square(self, n: int) -> Iterable[int]:
        """ return an iterable with indice of cells that belongs to square n
        >>> sudoku = Sudoku()
        >>> list(sudoku.square(1))
        [0, 1, 2, 9, 10, 11, 18, 19, 20]
        >>> list(sudoku.square(4))
        [27, 28, 29, 36, 37, 38, 45, 46, 47]
        >>> list(sudoku.square(9))
        [60, 61, 62, 69, 70, 71, 78, 79, 80]

        >>> sudoku2x2 = Sudoku(width=2)
        >>> list(sudoku2x2.square(1))
        [0, 1, 4, 5]
        >>> list(sudoku2x2.square(2))
        [2, 3, 6, 7]
        >>> list(sudoku2x2.square(3))
        [8, 9, 12, 13]
        >>> list(sudoku2x2.square(4))
        [10, 11, 14, 15]
        """
        row_offset = ((n - 1) // self.width) * self.width ** 3
        column_offset = ((n - 1) % self.width) * self.width
        start = row_offset + column_offset
        return itertools.chain.from_iterable(range(start + i * self.max_num, start + i * self.max_num + self.width) for i in range(self.width))

    def column(self, n: int) -> Iterable[int]:
        """ return an iterable with indice of cells that belongs to column n
        >>> sudoku = Sudoku()
        >>> list(sudoku.column(1))
        [0, 9, 18, 27, 36, 45, 54, 63, 72]
        >>> list(sudoku.column(9))
        [8, 17, 26, 35, 44, 53, 62, 71, 80]

        >>> sudoku2x2 = Sudoku(width=2)
        >>> list(sudoku2x2.column(1))
        [0, 4, 8, 12]
        >>> list(sudoku2x2.column(2))
        [1, 5, 9, 13]
        >>> list(sudoku2x2.column(3))
        [2, 6, 10, 14]
        >>> list(sudoku2x2.column(4))
        [3, 7, 11, 15]
        """
        return range((n-1), self.width ** 4, self.width ** 2)

    def cell_to_row(self, idx: int) -> int:
        """ return the row number of a cell
        >>> sudoku = Sudoku()
        >>> sudoku.cell_to_row(0)
        1
        >>> sudoku.cell_to_row(35)
        4
        >>> sudoku.cell_to_row(75)
        9

        >>> sudoku2x2 = Sudoku(width=2)
        >>> sudoku2x2.cell_to_row(4)
        2
        >>> sudoku2x2.cell_to_row(7)
        2
        >>> sudoku2x2.cell_to_row(10)
        3
        """
        return idx // self.max_num + 1

    def cell_to_column(self, idx: int) -> int:
        """ return the column number of a cell
        >>> sudoku = Sudoku()
        >>> sudoku.cell_to_column(0)
        1
        >>> sudoku.cell_to_column(24)
        7
        >>> sudoku.cell_to_column(49)
        5
        >>> sudoku.cell_to_column(74)
        3
        """
        return idx % self.width ** 2 + 1

    def cell_to_square(self, idx: int) -> int:
        """ return the square number of a cell
        >>> sudoku = Sudoku()
        >>> sudoku.cell_to_square(0)
        1
        >>> sudoku.cell_to_square(24)
        3
        >>> sudoku.cell_to_square(49)
        5
        >>> sudoku.cell_to_square(74)
        7

        >>> sudoku2x2 = Sudoku(width=2)
        >>> sudoku2x2.cell_to_square(0)
        1
        >>> sudoku2x2.cell_to_square(6)
        2
        >>> sudoku2x2.cell_to_square(12)
        3
        >>> sudoku2x2.cell_to_square(10)
        4
        """
        x_offset = (idx % self.width ** 2) // self.width + 1
        y_offset = (idx // self.width ** 3) * self.width
        return x_offset + y_offset

    def same_row_column_square(self, idx: int) -> list[int]:
        """ return an iterable of cells in same row/column/square.
        >>> sudoku = Sudoku()
        >>> set(sudoku.same_row_column_square(0))
        {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 27, 36, 45, 54, 63, 72}

        >>> set(sudoku.same_row_column_square(51))
        {6, 15, 24, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 60, 69, 78}

        >>> sudoku2x2 = Sudoku(width=2)
        >>> set(sudoku2x2.same_row_column_square(0))
        {0, 1, 2, 3, 4, 5, 8, 12}
        >>> set(sudoku2x2.same_row_column_square(6))
        {2, 3, 4, 5, 6, 7, 10, 14}
        >>> set(sudoku2x2.same_row_column_square(9))
        {1, 5, 8, 9, 10, 11, 12, 13}
        """
        r = self.cell_to_row(idx)
        c = self.cell_to_column(idx)
        s = self.cell_to_square(idx)
        return itertools.chain(self.row(r), self.column(c), self.square(s))

    def update_candidates(self, candidates: list[int], idx: int, number: int) -> list[int]:
        """
        update a list representation of number candidates in a sudoku.
        candidate are represented by bits.
        occupied cells are represented by negative nums
        e.g.:
        0: empty cell, all nums in 1-9 are valid
        3: ( = 0b000000011) empty cell, num 1 & 2 are not valid
        511: (= 0b111111111) empty cell, all nums in 1-9 are not valid
        -3: cell occupied by number 3
        >>> sudoku = Sudoku()
        >>> sudoku.update_candidates([0 for _ in range(81)], 0, 3)
        [-3, 4, 4, 4, 4, 4, 4, 4, 4,
        4, 4, 4, 0, 0, 0, 0, 0, 0,
        4, 4, 4, 0, 0, 0, 0, 0, 0,
        4, 0, 0, 0, 0, 0, 0, 0, 0,
        4, 0, 0, ... 0]
        """
        new_candidates = candidates.copy()
        for cell in self.same_row_column_square(idx):
            if (new_candidates[cell] >= 0):
                new_candidates[cell] |= (1 << (number - 1))
        new_candidates[idx] = -number
        return new_candidates

    def map_puzzle_to_candidates(self, puzzle: str) -> list[int]:
        """
        calculate the number candidates for each cell in a sudoku puzzle.
        valid numbers are represented by bits.
        e.g.:
        0: all nums in 1-9 are valid
        3: ( = 0b000000011) num 1 & 2 are not valid
        511: (= 0b111111111) all nums in 1-9 are not valid
        >>> puzzle = '..3..4.22.4..1.3'
        >>> sudoku2x2 = Sudoku(width=2)
        >>> sudoku2x2.map_puzzle_to_candidates(puzzle)
        [14, 13, -3, 6, 10, -4, 14, -2, -2, 11, -4, 14, 7, -1, 13, -3]
        """
        candidates = [0 for _ in range(self.max_num ** 2)]
        puzzle = puzzle.replace('.', '0')
        for idx in range(len(puzzle)):
            if puzzle[idx] != '0':
                candidates = self.update_candidates(
                    candidates, idx, int(puzzle[idx]))
        return candidates

    def fewest_candidate_cell(self, candidates: list[int]) -> int:
        """
        return the empty cell with fewest possible candidate, by counting bits and find the cell with highest bits.

        It should pick the cell with most 1s in binary representation.
        >>> sudoku = Sudoku()
        >>> candidates = [0b1100, 0b1101, 0b1001, 0b1111, 0b0011, 0b1001]
        >>> sudoku.fewest_candidate_cell(candidates)
        3
        >>> candidates2 = [1,3,5,7,9,12,2,31,4,5,32,4,6,15]
        >>> sudoku.fewest_candidate_cell(candidates2)
        7

        Any negative numbers should be ignored.
        >>> candidates3 = [1,3,5,7,12,-32,-1,-3,4]
        >>> sudoku.fewest_candidate_cell(candidates3)
        3

        Return None if all numbers are negagive.
        >>> candidates4 = [-1, -3, -32, -7, -9, -1]
        >>> print(sudoku.fewest_candidate_cell(candidates4))
        None
        """
        fewest = None
        highest_bits = -1
        for cell in range(0, len(candidates)):
            if candidates[cell] >= 0 and count_bit(candidates[cell]) > highest_bits:
                fewest = cell
                highest_bits = count_bit(candidates[cell])
        return fewest

    def start_solve(self, puzzle: str):
        """
        solve a sudoku puzzle by backtracking.
        >>> puzzle1 = "123434122341412."
        >>> sudoku2x2 = Sudoku(width=2)
        >>> sudoku2x2.start_solve(puzzle1)
        found solution: [[1, 2, 3, 4, 3, 4, 1, 2, 2, 3, 4, 1, 4, 1, 2, 3]]

        >>> puzzle2 = "12343412........"
        >>> sudoku2x2 = Sudoku(width=2)
        >>> sudoku2x2.start_solve(puzzle2)
        found solution: [[1, 2, 3, 4, 3, 4, 1, 2, 2, 1, 4, 3, 4, 3, 2, 1], [1, 2, 3, 4, 3, 4, 1, 2, 2, 3, 4, 1, 4, 1, 2, 3]]
        """
        # if not validate_str(puzzle):
        #     raise ValueError('cannot interpret this sudoku string')

        candidates = self.map_puzzle_to_candidates(puzzle)
        if any(candidate == 2 ** self.max_num - 1 for candidate in candidates):
            print('puzzle is unsolvable')
            return None

        solutions = self.solve(candidates)
        if solutions:
            print('found solution:', solutions)
        else:
            print('no solution was found.')

    def solve(self, candidates: list[int]):
        cell_to_try = self.fewest_candidate_cell(candidates)
        if cell_to_try == None:
            # no empty cells.
            # i.e. a solution is found.
            solution = [-i for i in candidates]
            return [solution]

        bit = candidates[cell_to_try]
        if bit == 2 ** self.max_num - 1:
            # found an empty cell which cannot fit any number.
            # i.e. puzzle is unsolvable at this point
            # do a backtrack at such situation
            return None

        solutions = []
        number_to_try = 1
        while number_to_try <= self.max_num:
            if bit & 1 != 0:
                # last bit = 1. i.e. this cell can't have this num.
                pass
            else:
                # last bit = 0. try to put this number into the cell.
                new_candidates = self.update_candidates(
                    candidates, cell_to_try, number_to_try)
                solution_found = self.solve(new_candidates)
                if solution_found:
                    solutions += solution_found
                if len(solutions) > 1:
                    # more than one solution found
                    return solutions
            number_to_try += 1
            bit >>= 1
        return solutions


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS |
                    doctest.NORMALIZE_WHITESPACE)
