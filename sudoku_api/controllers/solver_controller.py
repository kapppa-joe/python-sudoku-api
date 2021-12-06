from flask import request, abort, make_response
from flask_restful import Resource
from marshmallow import Schema, fields
from result import Ok, Err

from sudoku_api.models.solver_model import solve_puzzle
from sudoku_api.core.display import display_grid


class Solver(Resource):
    def get(self):
        return {"message": "POST a Sudoku puzzle to this url and I will solve it for you! :)"}

    def post(self):
        if not request.get_json() and not request.form:
            return {"message": {
                'puzzle': ['Missing data for required field.']}}, 400

        body = request.get_json(silent=True, force=True)
        if not body:
            body = request.form

        errors = solver_request_schema.validate(body)
        if errors:
            abort(400, errors)

        body = solver_request_schema.load(body)

        puzzle = body.get('puzzle')
        display_as_grid = body.get('display_as_grid')
        result = solve_puzzle(puzzle)
        match result:
            case Ok(solutions):
                if len(solutions) == 1:
                    if display_as_grid:
                        res = make_response(display_grid(solutions[0]), 200)
                        res.mimetype = 'text/plain'
                        return res

                    return {"solution": solutions[0]}
                else:
                    return {"solution": solutions[0], "alternative_solution": solutions[1], "message": "more than 1 solution found for given puzzle. only returning the first two solutions found."}
            case Err(msg):
                return {"message": msg}, 400


class SolverRequestSchema(Schema):
    puzzle = fields.Str(required=True)
    display_as_grid = fields.Bool()


solver_request_schema = SolverRequestSchema()
