from flask_restful import Resource, reqparse
from sudoku_api.models.solver_model import solve_puzzle
from result import Ok, Err


parser = reqparse.RequestParser()
parser.add_argument('puzzle')


class Solver(Resource):
    def get(self):
        return {"msg": "POST a Sudoku puzzle to this url and I will solve it for you! :)"}

    def post(self):
        args = parser.parse_args()
        puzzle = args["puzzle"]
        if not puzzle:
            return {"msg": r"sorry, only accept a body with format {puzzle: str}, where str is a string of 81 digits representing a Sudoku puzzle"}, 400

        result = solve_puzzle(puzzle)
        match result:
            case Ok(solutions):
                if len(solutions) == 1:
                    return {"solution": solutions[0]}
                else:
                    return {"solution": solutions[0], "alternative_solution": solutions[1], "msg": "more than 1 solution found for given puzzle. only returning the first two solutions found."}
            case Err(msg):
                return {"msg": msg}, 400
