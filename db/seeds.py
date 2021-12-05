# This file should contain records you want created when you run flask db seed.
#

# ===== seeds script for importing puzzles from seed file

from app import db
from sudoku_api.models.Puzzle import PuzzleSchema

schema = PuzzleSchema(many=True)
seeds = None
with open('db/seeds.json', 'r') as f:
    file = f.read()
    seeds = schema.loads(file)
for puzzle in seeds:
    db.session.add(puzzle)
db.session.commit()

# # ===== seeds script for generating new puzzles from scratch =====
# from sudoku_api.models.Puzzle import generate_puzzles
# from app import db
# puzzles = generate_puzzles()
# for p in puzzles:
#     db.session.add(p)
# db.session.commit()
