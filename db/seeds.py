# This file should contain records you want created when you run flask db seed.
#

from sudoku_api.models.Puzzle import generate_puzzles
from app import db
puzzles = generate_puzzles()
for p in puzzles:
    db.session.add(p)
db.session.commit()
