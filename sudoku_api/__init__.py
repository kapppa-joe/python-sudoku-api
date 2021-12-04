from flask import Flask
from flask_restful import Resource, Api
# from flask_marshmallow import Marshmallow
from config import Config
from sudoku_api.database import db
from sudoku_api.models.serializer import configure_marshmallow


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.from_mapping(test_config)
    db.init_app(app)
    configure_marshmallow(app)

    from sudoku_api.controllers.solver_controller import Solver
    from sudoku_api.controllers.puzzles_controller import Puzzle

    api = Api(app)
    api.add_resource(HelloWorld, '/')
    api.add_resource(Solver, '/solver')
    api.add_resource(Puzzle, '/puzzles', '/puzzles/<int:puzzle_id>')
    return app
