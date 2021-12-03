from sudoku_api import create_app


def test_config():
    assert not create_app().testing
    assert create_app(
        {'TESTING': True, 'SQLALCHEMY_TRACK_MODIFICATIONS': False}).testing


def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"hello": "world"}
