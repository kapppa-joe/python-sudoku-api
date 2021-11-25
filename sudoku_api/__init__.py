from sudoku_api.controllers.solver_controller import Solver
from flask_restful import Resource, Api
from flask import Flask


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    api = Api(app)
    api.add_resource(HelloWorld, '/')
    api.add_resource(Solver, '/solver')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
