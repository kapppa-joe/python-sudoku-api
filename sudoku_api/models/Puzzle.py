from typing import Tuple
from sudoku_api.database import db
from sudoku_api.core import Sudoku
from sudoku_api.models.serializer import ma
from marshmallow import post_load


class Puzzle(db.Model):  # type: ignore
    __tablename__ = 'puzzles'

    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    puzzle = db.Column(db.Text, nullable=False)  # type: ignore
    solution = db.Column(db.Text, nullable=False)  # type: ignore
    difficulty = db.Column(db.Integer, nullable=False)  # type: ignore
    size = db.Column(db.String(3), nullable=False,  # type: ignore
                     default="3x3")  # type: ignore

    def __repr__(self):
        return f'<Puzzle {self.puzzle}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PuzzleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Puzzle

    @post_load
    def make_puzzle(self, data, **kwargs):
        return Puzzle(**data)


puzzle_schema = PuzzleSchema()


def to_json(p: Puzzle):
    return puzzle_schema.dump(p)


def get_puzzles(**kwargs) -> Tuple[list, int]:
    filters = []
    limit = kwargs.get("limit", 10)
    offset = kwargs.get("offset", 0)
    sort_by = kwargs.get("sort_by", 'id')
    order = kwargs.get("order", 'asc')

    for (key, value) in kwargs.items():
        match key:
            case "min_difficulty":
                filters.append(Puzzle.difficulty >= value)
            case "max_difficulty":
                filters.append(Puzzle.difficulty <= value)
            case "size":
                filters.append(Puzzle.size == value)

    match (sort_by, order):
        case ('id', 'desc'):
            order = Puzzle.id.desc()
        case ('difficulty', 'asc'):
            order = Puzzle.difficulty.asc()
        case ('difficulty', 'desc'):
            order = Puzzle.difficulty.desc()
        case _:
            order = Puzzle.id.asc()

    raw_query_result = Puzzle.query.filter(*filters)
    total_count = raw_query_result.count()
    query_result = raw_query_result.order_by(
        order).limit(limit).offset(offset)
    return ([to_json(puzzle) for puzzle in query_result], total_count)


def get_puzzle_by_id(id: int):
    puzzle = Puzzle.query.filter_by(id=id).first_or_404()
    return puzzle_schema.dump(puzzle)


def generate_puzzles(width: int = 3, height: int = 3, number: int = 20, min_difficulty=0) -> list[Puzzle]:
    if number < 1:
        return []
    sudoku = Sudoku(width=width, height=height)
    puzzles = []
    for _ in range(number):
        (puzzle, solution, score) = sudoku.generate_puzzle(
            min_difficulty=min_difficulty)
        puzzles.append(Puzzle(puzzle=puzzle, solution=solution,
                       difficulty=score, size=f'{width}x{height}'))
    return puzzles
