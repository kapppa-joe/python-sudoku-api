from sudoku_api.database import db


class Puzzle(db.Model):
    __tablename__ = 'puzzles'

    id = db.Column(db.Integer, primary_key=True)
    puzzle = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(3), nullable=False, default="3x3")

    def __repr__(self):
        return f'<Puzzle {self.puzzle}>'
