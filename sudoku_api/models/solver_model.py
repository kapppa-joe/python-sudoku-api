from sudoku_api.core.sudoku import Sudoku


def solve_puzzle(puzzle: str):
    solver = Sudoku()
    result = solver.solve_puzzle(puzzle)
    return result
