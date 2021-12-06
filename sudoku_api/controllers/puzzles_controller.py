from typing import Dict, Optional, Any
from flask import request, abort
from flask_restful import Resource
from marshmallow import Schema, fields, validate, ValidationError

from sudoku_api.models.Puzzle import get_puzzles, get_puzzle_by_id


class Puzzle(Resource):
    def get(self, puzzle_id: Optional[int] = None) -> Dict[str, Any]:
        if puzzle_id != None:
            puzzle = get_puzzle_by_id(puzzle_id)
            return {"puzzle": puzzle}
        else:
            errors = puzzle_query_schema.validate(request.args)
            if errors:
                abort(400, str(errors))

            kwargs = request.args.to_dict()
            (puzzles, total_count) = get_puzzles(**kwargs)
            return {"puzzles": puzzles, "total_count": total_count}


def is_valid_puzzle_size(size: str):
    try:
        (w, h) = size.split('x')
        if int(w) < 2 or int(w) > 9 or int(h) < 2 or int(w) > 9:
            raise
    except:
        raise ValidationError(
            "Size of puzzle must be in the format AxB, where A, B are integers between 2-9.")


class PuzzleQuerySchema(Schema):
    min_difficulty = fields.Int(validate=validate.Range(
        min=0, max=1000, error="Difficulty must be between 0 and 1000."))
    max_difficulty = fields.Int(validate=validate.Range(
        min=0, max=1000, error="Difficulty must be between 0 and 1000."))
    size = fields.Str(validate=is_valid_puzzle_size)
    limit = fields.Int(validate=validate.Range(
        min=10, error="Must be 10 or above."))
    offset = fields.Int(validate=validate.Range(
        min=0, error="Must be 0 or above."))
    sort_by = fields.Str(validate=validate.OneOf(
        ["id", "difficulty"], error="Can only sort by either id or difficulty."))
    order = fields.Str(validate=validate.OneOf(
        ["asc", "desc"], error="Can only accept order of asc or desc."))


puzzle_query_schema = PuzzleQuerySchema()
