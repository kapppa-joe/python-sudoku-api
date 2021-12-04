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
    app.db = db
    ma = configure_marshmallow(app)
    # ma = Marshmallow(app)
    # app.ma = ma

    from sudoku_api.controllers.solver_controller import Solver
    from sudoku_api.controllers.puzzles_controller import Puzzle

    api = Api(app)
    api.add_resource(HelloWorld, '/')
    api.add_resource(Solver, '/solver')
    api.add_resource(Puzzle, '/puzzles')
    return app

# def create_app(test_config=None):
#     # from sudoku_api.models.Puzzles import db
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     if test_config is None:
#         app.config.from_pyfile('config.py', silent=False)
#     else:
#         app.config.from_mapping(test_config)

#     # db.init_app(app)
#     return app


# def init_db():
#     from sudoku_api.models.Puzzles import db
#     db.create_all()


# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)
