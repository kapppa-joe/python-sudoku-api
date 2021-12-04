from sudoku_api.database import db
from sudoku_api.core import Sudoku
from sudoku_api.models.serializer import ma


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

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PuzzleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Puzzle


puzzle_schema = PuzzleSchema()


def to_json(p: Puzzle):
    return puzzle_schema.dump(p)


def get_puzzles(**kwargs):
    filters = []
    limit = kwargs.get("limit", 10)
    offset = kwargs.get("offset", 0)
    for (key, value) in kwargs.items():
        match key:
            case "min_difficulty":
                filters.append(Puzzle.score >= value)
            case "max_difficulty":
                filters.append(Puzzle.score <= value)
            case "size":
                filters.append(Puzzle.size == value)

    query_result = Puzzle.query.filter(*filters).limit(limit).offset(offset)
    # print([puzzle.as_dict()["id"] for puzzle in query_result2])
    return [puzzle.as_dict() for puzzle in query_result]


def get_puzzle_by_id(id: int):
    puzzle = Puzzle.query.filter_by(id=id).first_or_404()
    return puzzle_schema.dump(puzzle)


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
