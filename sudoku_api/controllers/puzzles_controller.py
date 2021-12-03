from flask_restful import Resource, reqparse
from sudoku_api import db
from result import Ok, Err
from flask import jsonify
from sudoku_api.models.Puzzle import get_puzzles


parser = reqparse.RequestParser()
parser.add_argument('puzzle')


class Puzzle(Resource):
    def get(self):
        puzzles = get_puzzles()
        return {"puzzles": puzzles}
