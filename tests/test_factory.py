from sudoku_api import create_app


def test_config():
    assert not create_app().testing
    assert create_app(
        {'TESTING': True, 'SQLALCHEMY_TRACK_MODIFICATIONS': False}).testing


def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"hello": "world"}


def test_intro(client):
    response = client.get('/api')
    assert response.status_code == 200
    assert response.json == {
        "message": "Welcome to sudoku-api! Please visit https://github.com/kapppa-joe/python-sudoku-api for how to interact with this API service."}
