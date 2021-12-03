from sudoku_api.database import db
from sudoku_api.core import Sudoku


class Puzzle(db.Model):  # type: ignore
    __tablename__ = 'puzzles'

    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    puzzle = db.Column(db.Text, nullable=False)  # type: ignore
    solution = db.Column(db.Text, nullable=False)  # type: ignore
    score = db.Column(db.Integer, nullable=False)  # type: ignore
    size = db.Column(db.String(3), nullable=False,  # type: ignore
                     default="3x3")  # type: ignore

    def __repr__(self):
        return f'<Puzzle {self.puzzle}>'


def generate_puzzles(width: int = 3, height: int = 3, number: int = 20) -> list[Puzzle]:
    if number < 1:
        return []
    sudoku = Sudoku(width=width, height=height)
    puzzles = []
    for _ in range(number):
        (puzzle, solution, score) = sudoku.generate_puzzle()
        puzzles.append(Puzzle(puzzle=puzzle, solution=solution,
                       score=score, size=f'{width}x{height}'))
    return puzzles
