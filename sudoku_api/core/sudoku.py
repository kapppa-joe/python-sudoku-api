import itertools
import random
from typing import Iterable, Optional, Tuple
from sudoku_api.core.utils import conv_bit_to_num_list, count_bit, all_unique, replace_string, sofa_find_candidate
from result import Ok, Err, Result


class Sudoku():
    def __init__(self, width: int = 3, height: int = None):
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
        self.height = height or self.width
        self.max_num = width ** 2
        self.number_of_cells = width ** 4

    def validate_puzzle_string(self, puzzle: str) -> Result[bool, str]:
        """ Validate a string as a representation of Sudoku puzzle
        accept 0 or . to represent an empty cell
        DOES NOT check whether if it is a valid answer in Sudoku

        Return False for empty input
        >>> sudoku = Sudoku()
        >>> sudoku.validate_puzzle_string('')
        Err('The length of puzzle is not correct. Should have exactly 81 chars.')

        Return True for any combination of . and 1-9 with length 81
        >>> sudoku.validate_puzzle_string('..9..5.1.85.4....2432......1...69.83.9.....6.62.71...9......1945....4.37.4.3..6..')
        Ok(True)

        Return False if length is not exactly 81
        >>> sudoku.validate_puzzle_string('..9..5.1.85.4....2432......1...69.83.9.....6.62.71...9......1945....4.37.4.3..6..1')
        Err('The length of puzzle is not correct. Should have exactly 81 chars.')

        Return False if any of the char are not . or 1-9
        >>> sudoku.validate_puzzle_string('A.9..5.1.85.4...2432......1...69.83.9.....6.62.71...9......1945....4.37.4.3..6..1')
        Err('Invalid char in puzzle. Can only contain 0, . or number 1-9')

        Return False if duplicated number in same row/column/square
        >>> sudoku.validate_puzzle_string('113456789' + '0' * 72)
        Err('Duplicated number found in row/column/square.')

        # For case of 2x2 puzzle, check for length = 16 and each char being 0-4.
        # >>> sudoku2x2 = Sudoku(width=2)
        # >>> sudoku2x2.validate_puzzle_string('12343412234141..')
        # True
        # >>> sudoku2x2.validate_puzzle_string('12343412234141..1')
        # False
        # >>> sudoku2x2.validate_puzzle_string('12343412234141.')
        # False
        # >>> sudoku2x2.validate_puzzle_string('1234341223414A..')
        # False
        """
        if len(puzzle) != self.number_of_cells:
            return Err(f'The length of puzzle is not correct. Should have exactly {self.number_of_cells} chars.')
        elif not all(char == '.' or (char.isnumeric() and int(char) <= self.max_num) for char in puzzle):
            return Err(f'Invalid char in puzzle. Can only contain 0, . or number 1-{self.max_num}')
        elif not self.numbers_are_unique(puzzle):
            return Err('Duplicated number found in row/column/square.')
        else:
            return Ok()

    def numbers_are_unique(self, puzzle: str) -> bool:
        """
        verify whether every number in row/column/square is unique.
        does strip out . and 0 before checking for uniqueness

        >>> sudoku2x2 = Sudoku(width=2)
        >>> sudoku2x2.numbers_are_unique('1234341223414123')
        True
        >>> sudoku2x2.numbers_are_unique('1234000000000000')
        True
        >>> sudoku2x2.numbers_are_unique('1134000000000000')
        False
        >>> sudoku2x2.numbers_are_unique('1234100000000000')
        False
        >>> sudoku2x2.numbers_are_unique('1234010000000000')
        False
        """
        for iter in self.all_rows_columns_squares():
            numbers_in_cell = (num
                               for idx in iter if (num := puzzle[idx]) != '.' and num != '0')
            if not all_unique(numbers_in_cell):
                return False
        return True

    def validate_solution(self, solution: str | Iterable[int]) -> Result[bool, str]:
        """ check whether a solution is a valid sudoku.
        >>> sudoku2x2 = Sudoku(width=2)
        >>> sudoku2x2.validate_solution('1234')
        Err('The length of puzzle is not correct. Should have exactly 16 chars.')

        >>> sudoku2x2.validate_solution('1234341223414123')
        Ok(True)

        >>> sudoku2x2.validate_solution('1134341223414123')
        Err('Duplicated number found in row/column/square.')

        >>> sudoku2x2.validate_solution('5234341223414123')
        Err('Solution contain invalid char. Should only have number 1-4')

        >>> sudoku2x2.validate_solution('0234341223414123')
        Err('Solution contain invalid char. Should only have number 1-4')

        >>> sudoku2x2.validate_solution('.234341223414123')
        Err('Solution contain invalid char. Should only have number 1-4')
        """
        if isinstance(solution, Iterable):
            solution = ''.join(str(i) for i in solution)

        for cell in solution:
            if not (cell.isnumeric() and int(cell) > 0 and int(cell) <= self.max_num):
                return Err(f'Solution contain invalid char. Should only have number 1-{self.max_num}')
        result = self.validate_puzzle_string(solution)
        if isinstance(result, Err):
            return result
        return Ok()

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

    def all_rows_columns_squares(self) -> Iterable[Iterable[int]]:
        """
        return a nested iterable of cell numbers for all rows, columns, squares in a sudoku
        >>> sudoku2x2 = Sudoku(width=2)
        >>> [list(iter) for iter in sudoku2x2.all_rows_columns_squares()]
        [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15], [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [0, 1, 4, 5], [2, 3, 6, 7], [8, 9, 12, 13], [10, 11, 14, 15]] """
        return itertools.chain((self.row(i) for i in range(1, self.max_num + 1)), (self.column(i) for i in range(1, self.max_num + 1)), (self.square(i) for i in range(1, self.max_num + 1)))

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

    def same_row_column_square(self, idx: int) -> Iterable[int]:
        """ return an iterable of cells in same row/column/square.
        >>> sudoku = Sudoku()
        >>> set(sudoku.same_row_column_square(0))
        {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 27, 36, 45, 54, 63, 72}

        >>> set(sudoku.same_row_column_square(51))
        {6, 15, 24, 33, 34, 35, 42, 43, 44, 45, 46,
            47, 48, 49, 50, 51, 52, 53, 60, 69, 78}

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

    def update_grid(self, grid: list[int], idx: int, number: int) -> list[int]:
        """
        update a list representation of number candidates in a sudoku.
        candidates are represented by bits.
        occupied cells are represented by negative nums
        e.g.:
        0: empty cell, all nums in 1-9 are valid
        3: ( = 0b000000011) empty cell, num 1 & 2 are not valid
        511: (= 0b111111111) empty cell, all nums in 1-9 are not valid
        -3: cell occupied by number 3
        >>> sudoku = Sudoku()
        >>> sudoku.update_grid([0 for _ in range(81)], 0, 3)
        [-3, 4, 4, 4, 4, 4, 4, 4, 4,
        4, 4, 4, 0, 0, 0, 0, 0, 0,
        4, 4, 4, 0, 0, 0, 0, 0, 0,
        4, 0, 0, 0, 0, 0, 0, 0, 0,
        4, 0, 0, ... 0]
        """
        new_grid = grid.copy()
        for cell in self.same_row_column_square(idx):
            if (new_grid[cell] >= 0):
                new_grid[cell] |= (1 << (number - 1))
        new_grid[idx] = -number
        return new_grid

    def map_puzzle_to_grid(self, puzzle: str) -> list[int]:
        """
        calculate the number candidates for each cell in a sudoku puzzle.
        valid numbers are represented by bits.
        e.g.:
        0: all nums in 1-9 are valid
        3: ( = 0b000000011) num 1 & 2 are not valid
        511: (= 0b111111111) all nums in 1-9 are not valid
        >>> puzzle = '..3..4.22.4..1.3'
        >>> sudoku2x2 = Sudoku(width=2)
        >>> sudoku2x2.map_puzzle_to_grid(puzzle)
        [14, 13, -3, 6, 10, -4, 14, -2, -2, 11, -4, 14, 7, -1, 13, -3]
        """
        grid = [0 for _ in range(self.max_num ** 2)]
        puzzle = puzzle.replace('.', '0')
        for idx in range(len(puzzle)):
            if puzzle[idx] != '0':
                grid = self.update_grid(
                    grid, idx, int(puzzle[idx]))
        return grid

    def fewest_candidate_cell(self, grid: list[int]) -> Optional[int]:
        """
        return the empty cell with fewest possible candidate, by counting bits and find the cell with highest bits.

        It should pick the cell with most 1s in binary representation.
        >>> sudoku = Sudoku()
        >>> grid = [0b1100, 0b1101, 0b1001, 0b1111, 0b0011, 0b1001]
        >>> sudoku.fewest_candidate_cell(grid)
        3
        >>> grid2 = [1,3,5,7,9,12,2,31,4,5,32,4,6,15]
        >>> sudoku.fewest_candidate_cell(grid2)
        7

        Any negative numbers should be ignored.
        >>> grid3 = [1,3,5,7,12,-32,-1,-3,4]
        >>> sudoku.fewest_candidate_cell(grid3)
        3

        Return None if all numbers are negagive.
        >>> grid4 = [-1, -3, -32, -7, -9, -1]
        >>> print(sudoku.fewest_candidate_cell(grid4))
        None
        """
        fewest = None
        highest_bits = -1
        for cell in range(0, len(grid)):
            if grid[cell] >= 0 and count_bit(grid[cell]) > highest_bits:
                fewest = cell
                highest_bits = count_bit(grid[cell])
        return fewest

    def solve_puzzle(self, puzzle: str) -> Result[list[str], 'str']:
        """
        solve a sudoku puzzle by backtracking.
        >>> puzzle1 = "123434122341412."
        >>> sudoku2x2 = Sudoku(width=2)
        >>> sudoku2x2.solve_puzzle(puzzle1)
        Ok(['1234341223414123'])

        >>> puzzle2 = "12343412........"
        >>> sudoku2x2 = Sudoku(width=2)
        >>> result = sudoku2x2.solve_puzzle(puzzle2)
        >>> result
        Ok(['1234341221434321', '1234341223414123'])

        >>> solutions = result.ok()
        >>> sudoku2x2.validate_solution(solutions[0])
        Ok(True)
        >>> sudoku2x2.validate_solution(solutions[1])
        Ok(True)

        >>> puzzle3 = "..9..5.1.85.4....2432......1...69.83.9.....6.62.71...9......1945....4.37.4.3..6.."
        >>> sudoku = Sudoku()
        >>> sudoku.solve_puzzle(puzzle3)
        Ok(['76923541885...81625'])

        >>> puzzle4 = "123443123.....2."
        >>> sudoku2x2.solve_puzzle(puzzle4)
        Err('puzzle is unsolvable')

        >>> puzzle5 = "1234567894567891237801234562316740958759123646905382073172659485428976319683415A2"
        >>> sudoku.solve_puzzle(puzzle5)
        Err('Invalid char in puzzle. Can only contain 0, . or number 1-9')
        """

        validation_result = self.validate_puzzle_string(puzzle)
        if err_msg := validation_result.err():
            return Err(err_msg)

        grid = self.map_puzzle_to_grid(puzzle)
        if any(candidate == 2 ** self.max_num - 1 for candidate in grid):
            return Err('puzzle is unsolvable')

        solutions = self.solve(grid)
        if solutions:
            return Ok(solutions)
        else:
            return Err('no solution was found.')

    def solve(self, grid: list[int]) -> list[str]:
        cell_to_try = self.fewest_candidate_cell(grid)
        if cell_to_try == None:
            # no empty cells.
            # i.e. a solution is found.
            solution = ''.join(str(-i) for i in grid)
            return [solution]

        bit = grid[cell_to_try]
        if bit == 2 ** self.max_num - 1:
            # found an empty cell which cannot fit any number.
            # i.e. puzzle is unsolvable at this point
            # do a backtrack at such situation
            return []

        solutions = []
        number_to_try = 1
        while number_to_try <= self.max_num:
            if bit & 1 != 0:
                # last bit = 1. i.e. this cell can't have this num.
                pass
            else:
                # last bit = 0. try to put this number into the cell.
                new_grid = self.update_grid(
                    grid, cell_to_try, number_to_try)
                solution_found = self.solve(new_grid)
                if solution_found:
                    solutions += solution_found
                if len(solutions) > 1:
                    # more than one solution found
                    return solutions
            number_to_try += 1
            bit >>= 1
        return solutions

    def evaluate_difficulty(self, puzzle: str, solution: str | None = None) -> Result[int, str]:
        """
        Calculate a difficulty score of a puzzle using an algorithm in this article https://dlbeer.co.nz/articles/sudoku.html
        The difficulty score consists of two parts:
        1. For the branching factor Bi of each node, summing (Bi - 1)^2. The total is branch difficulty score B
        2. Count the empty cells E at the start.
        Final score is given by B * 100 + E.

        Due to limit of time & knowledge, here I used an simple implementation, which do not take in count the techniques used by human solvers. (i.e. 'set oriented freedom analysis' not implemented)

        >>> very_easy_puzzle = "600037500030200704070018000059100203040372050007800001000004006700620000260503907"
        >>> medium_puzzle = "000000270008270045040000008000567010005009007000040000200000401900010000650304792"
        >>> very_hard_puzzle = "090004013460000207070000000150000390000058000600900005000740500000006109540000020"
        >>> unsolvable_puzzle = "620037500030200704070018000059100203040372050007800001000004006700620000260503907"
        >>> non_unique_puzzle = "123456789" + '0' * 72
        >>>
        >>> solver = Sudoku()
        >>> solver.evaluate_difficulty(very_easy_puzzle)
        Ok(46)
        >>> solver.evaluate_difficulty(medium_puzzle)
        Ok(752)
        >>> solver.evaluate_difficulty(very_hard_puzzle)
        Ok(1254)
        >>> solver.evaluate_difficulty(unsolvable_puzzle)
        Err('puzzle is unsolvable')
        >>> solver.evaluate_difficulty(non_unique_puzzle)
        Err('solution to this puzzle is not unique')
        """

        grid = self.map_puzzle_to_grid(puzzle)
        if not solution:
            res = self.solve_puzzle(puzzle)
            match res:
                case Err():
                    return Err("puzzle is unsolvable")
                case Ok(solutions):
                    if len(solutions) > 1:
                        return Err('solution to this puzzle is not unique')
                    else:
                        solution = solutions[0]
        if solution == None:
            return Err("puzzle is unsolvable")

        empty_cells_score = sum(1 for cell in grid if cell >= 0)
        branching_factors_score = 0

        next_cell = self.fewest_candidate_cell(grid)
        while next_cell != None:
            bit = grid[next_cell]
            branching_factor = self.max_num - count_bit(bit)
            branching_factors_score += ((branching_factor - 1) ** 2) * 100
            grid = self.update_grid(grid, next_cell, int(solution[next_cell]))
            next_cell = self.fewest_candidate_cell(grid)

        solution_2 = ''.join(str(-i) for i in grid)
        if solution != solution_2:
            raise RuntimeError("unknown error in calculating difficulty")

        total_score = empty_cells_score + branching_factors_score
        return Ok(total_score)

    def has_unique_solution(self, puzzle: str) -> bool:
        """
        check whether a puzzle has an unique solution.
        """
        try_solve = self.solve_puzzle(puzzle)
        count_solutions = len(try_solve.unwrap_or([]))
        return count_solutions == 1

    def random_digit_list(self) -> list[int]:
        """
        return a random shuffled list of numbers allowed in a row/column/square
        >>> sudoku = Sudoku()
        >>> list1 = sudoku.random_digit_list()
        >>> len(list1)
        9
        >>> all((i in list1)for i in range(1, 9))
        True
        >>> random.seed('test')
        >>> sudoku.random_digit_list()
        [7, 3, 6, 8, 9, 1, 2, 4, 5]
        >>> random.seed('test2')
        >>> sudoku.random_digit_list()
        [5, 9, 4, 2, 8, 3, 1, 6, 7]
        """
        num_list = [i for i in range(1, self.max_num + 1)]
        random.shuffle(num_list)
        return num_list

    def available_numbers(self, bit: int) -> list[int]:
        """
        convert a bit notation of candidates to a list of number
        >>> sudoku = Sudoku()
        >>> sudoku.available_numbers(bit=0)
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> sudoku.available_numbers(bit=3)
        [3, 4, 5, 6, 7, 8, 9]
        >>> sudoku.available_numbers(bit=50)
        [1, 3, 4, 7, 8, 9]
        """
        if bit < 0:
            return []
        elif bit == 0:
            return [i for i in range(1, self.max_num + 1)]
        else:
            numbers_taken = conv_bit_to_num_list(bit)
            return [i for i in range(1, self.max_num + 1) if not i in numbers_taken]

    def random_solver(self, grid: list[int]) -> list[int]:
        """
        randomly generate a complete sudoku grid from a partially filled grid
        """
        next_cell = self.fewest_candidate_cell(grid)
        if next_cell == None:
            return grid

        bit = grid[next_cell]
        if bit == 2 ** self.max_num - 1:
            return []

        number_choices = self.available_numbers(bit)
        random.shuffle(number_choices)
        while number_choices:
            number_to_try = number_choices.pop()
            new_grid = self.update_grid(grid, next_cell, number_to_try)
            solution_found = self.random_solver(new_grid)
            if solution_found:
                return solution_found
        return []

    # def sofa(self, grid: list[int]) -> list[int]:
    #     """ set-oriented freedom analysis
    #     # todo: run a naive solver, add a step to check sofa until n = lowest candidate num
    #     """

    def fewest_candidate_sofa_set(self, grid: list[int], upper_limit: int) -> Optional[Tuple[int, list[int]]]:
        """
        Traverse all the sets(=rows/columns/squares) in grid, and find a number which has the fewest possible position to take in a set
        related to the concept of 'set-oriented freedom analysis' and 'hidden single'
        >>> sofa_puzzle = "534008010000002090000007604000500100100000003009001000305400000080200000060700382"
        >>> sudoku = Sudoku()
        >>> grid = sudoku.map_puzzle_to_grid(sofa_puzzle)
        >>> sudoku.fewest_candidate_sofa_set(grid, 3)
        (2, [6])
        """

        number = None
        possible_pos_in_grid = None

        for cells_iter in self.all_rows_columns_squares():
            cell_idxs_in_set = list(cells_iter)
            bits = [grid[idx] for idx in cell_idxs_in_set]
            candidate = sofa_find_candidate(bits, upper_limit, self.max_num)
            if candidate:
                (number, possible_positions) = candidate
                possible_pos_in_grid = [cell_idxs_in_set[i]
                                        for i in possible_positions]
                if len(possible_positions) == 1:
                    break  # return early if a number got only 1 free cell available
                else:
                    upper_limit = len(possible_positions)
        if (number and possible_pos_in_grid):
            return (number, possible_pos_in_grid)
        else:
            return None

    def generate_puzzle(self, seed=None) -> str:
        if not seed == None:
            random.seed(seed)

        solution = self.generate_random_solution()
        base_puzzle = self.make_hole(solution)
        puzzle = self.adjust_puzzle(
            base_puzzle, solution, target_difficulty=1000)
        return puzzle

    def generate_random_solution(self) -> str:
        """
        Generate a random Sudoku grid which is a valid solution.
        """
        first_row = self.random_digit_list()
        grid = [0 for _ in range(self.number_of_cells)]
        for (idx, number) in enumerate(first_row):
            grid = self.update_grid(grid, idx, number)
        filled_grid = self.random_solver(grid)
        solution = ''.join(str(-i) for i in filled_grid)
        return solution

    def make_hole(self, p0: str) -> str:
        """
        randomly put 0s into filled grid to create a base puzzle to start from. check the puzzle to have unique solution before returning.
        """
        k = self.max_num * self.width // 2  # pairs of empty cell to take away from initially

        for _ in range(100):
            cell_indices = list(range(self.number_of_cells // 2))
            cells_to_remove = random.sample(cell_indices, k)
            # also remove the cell which is rotational counterpart
            cells_to_remove += [self.rotational_counterpart(idx)
                                for idx in cells_to_remove]
            p1 = ''.join(
                '0' if idx in cells_to_remove else p0[idx] for idx in range(len(p0)))
            if self.has_unique_solution(p1):
                return p1

        # if after 100 trials still cannot get a puzzle with unique solutions:
        raise RuntimeError('Error in generating puzzle.')

    def rotational_counterpart(self, idx: int) -> int:
        """
        return the cell idx of rotational counterpart of a cell
        >>> sudoku = Sudoku()
        >>> sudoku.rotational_counterpart(0)
        80
        >>> sudoku.rotational_counterpart(50)
        30
        >>> sudoku2x2 = Sudoku(width=2)
        >>> sudoku2x2.rotational_counterpart(0)
        15
        """
        if idx >= 0 and idx < self.number_of_cells:
            return self.number_of_cells - 1 - idx
        else:
            return 0

    def adjust_puzzle(self, base_puzzle: str, solution: str, target_difficulty: int) -> str:
        res = self.evaluate_difficulty(base_puzzle)
        if res.is_err():
            raise RuntimeError(res.err())
        p0_score = res.unwrap_or(0)
        p0 = base_puzzle
        print("p0 score:", p0_score)

        for _ in range(200):
            if p0_score < target_difficulty:
                idx = random.randint(0, len(p0) - 1)
                while p0[idx] == '0':
                    idx = random.randint(0, len(p0) - 1)
                p1 = replace_string(p0, idx, '0')
            else:
                idx = random.randint(0, len(p0) - 1)
                while p0[idx] != '0':
                    idx = random.randint(0, len(p0) - 1)
                p1 = replace_string(p0, idx, solution[idx])

            p1_score = self.evaluate_difficulty(p1).unwrap_or(0)
            if p1_score and abs(p1_score - target_difficulty) < abs(p0_score - target_difficulty):
                p0 = p1
                p0_score = p1_score
            if abs(p0_score - target_difficulty) < 50:
                return p0
        return p0


if __name__ == "__main__":
    sudoku = Sudoku()
    puzzle = '000000270008270045040000008000567010005009007000040000200000401900010000650304792'
    solution = '516438279398276145742951368823567914465129837179843526237695481984712653651384792'
    sudoku.evaluate_difficulty(puzzle, solution)
