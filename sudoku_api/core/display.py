from typing import Iterable


Hline = '-'
Vline = '|'
Cross = '+'


def draw_line(width: int, height: int) -> str:
    return (Hline * (width * 2 + 1)).join([Cross] * (height + 1))


def draw_sep_around(input: list[str], sep: str) -> str:
    """ add separator around each element in list
    >>> draw_sep_around(['12', '34', '56'], '|')
    '|12|34|56|'
    """
    return sep + sep.join(input) + sep


def draw_row(puzzle_row: str, width: int) -> str:
    """ draw a single row of the grid table
    >>> draw_row('1234', 2)
    '| 1 2 | 3 4 |'
    >>> draw_row('123456789', 3)
    '| 1 2 3 | 4 5 6 | 7 8 9 |'
    """
    block = []
    for start in range(0, len(puzzle_row), width):
        block.append(draw_sep_around(
            [digit for digit in puzzle_row[start:start+width]], ' '))
    return draw_sep_around(block, Vline)


def display_grid(puzzle: str, width: int = 3, height: int = 3) -> str:
    """
    Display a sudoku puzzle in ASCII art grid

    >>> print(display_grid("1234341223414123", 2, 2))
    +-----+-----+
    | 1 2 | 3 4 |
    | 3 4 | 1 2 |
    +-----+-----+
    | 2 3 | 4 1 |
    | 4 1 | 2 3 |
    +-----+-----+
    """
    if len(puzzle) != width * width * height * height:
        raise ValueError(
            'the length of puzzle string does not match the required size')
    # replace 0 with . for readability
    puzzle = puzzle.replace('0', '.')

    grid = []
    numbers_per_line = width * height
    line = draw_line(width, height)

    grid.append(line)
    puzzle_rows = [puzzle[i: i + numbers_per_line]
                   for i in range(0, len(puzzle), numbers_per_line)]
    # print(puzzle_rows)
    for i in range(width * height):
        grid.append(draw_row(puzzle_rows[i], width))
        if (i + 1) % height == 0:
            grid.append(line)
    return "\n".join(grid)
