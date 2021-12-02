import pytest
from sudoku_api import app as flask_app


@pytest.fixture
def app():
    return flask_app


@pytest.fixture
def client(app):
    test_client = app.test_client()

    return test_client
    # return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
