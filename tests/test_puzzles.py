from sudoku_api.core import Sudoku

sudoku = Sudoku()


def test_puzzles_get(client):
    # 200: return with a list of sudoku puzzles
    response = client.get('/puzzles')
    assert response.status_code == 200

    data = response.json["puzzles"]
    # default return a puzzle with 3x3 size, i.e. 81 cells
    for puzzle in data:
        assert type(puzzle["id"]) == int
        assert type(puzzle["puzzle"]) == str
        assert type(puzzle["solution"]) == str
        assert type(puzzle["score"]) == int
        assert type(puzzle["size"]) == str

    # puzzle should have a unique solution
    puzzle1 = data[0]
    assert sudoku.has_unique_solution(puzzle1["puzzle"]) == True
    assert sudoku.solve_puzzle(puzzle1["puzzle"]).unwrap()[
        0] == puzzle1["solution"]


def test_puzzles_get_with_query(client):
    # min_difficulty
    # 200: response with puzzles with scores >= min_difficulty
    response = client.get('/puzzles?min_difficulty=100')
    assert response.status_code == 200
    assert len(response.json["puzzles"]) > 0
    for puzzle in response.json["puzzles"]:
        assert puzzle["score"] >= 100

    # 400: min_difficulty must be an integer between 0 and 1000
    response = client.get('/puzzles?min_difficulty=-100')
    assert response.status_code == 400
    assert response.json["message"] == "{'min_difficulty': ['Difficulty must be between 0 and 1000.']}"
    response = client.get('/puzzles?min_difficulty=foo')
    assert response.status_code == 400
    assert response.json["message"] == "{'min_difficulty': ['Not a valid integer.']}"

    # max_difficulty
    # 200: response with puzzles with scores <= max_difficulty
    response = client.get('/puzzles?max_difficulty=100')
    assert response.status_code == 200
    assert len(response.json["puzzles"]) > 0
    for puzzle in response.json["puzzles"]:
        assert puzzle["score"] <= 100

    # 400: max_difficulty must be an integer between 0 and 1000
    response = client.get('/puzzles?max_difficulty=2000')
    assert response.status_code == 400
    assert response.json["message"] == "{'max_difficulty': ['Difficulty must be between 0 and 1000.']}"
    response = client.get('/puzzles?max_difficulty=bar')
    assert response.status_code == 400
    assert response.json["message"] == "{'max_difficulty': ['Not a valid integer.']}"

    # size
    # 200: different size puzzle not implement yet
    # 400: size must be in form of AxB
    response = client.get('/puzzles?size=9')
    assert response.status_code == 400
    assert response.json["message"] == "{'size': ['Size of puzzle must be in the format AxB, where A, B are integers between 2-9.']}"
    response = client.get('/puzzles?size=large')
    assert response.status_code == 400
    assert response.json["message"] == "{'size': ['Size of puzzle must be in the format AxB, where A, B are integers between 2-9.']}"

    # limit
    # 200: response with a list of puzzles with max length = limit
    # 400: limit must be 10 or above
    response = client.get('/puzzles?limit=5')
    assert response.status_code == 400
    assert response.json["message"] == "{'limit': ['Must be 10 or above.']}"
    response = client.get('/puzzles?limit=orange')
    assert response.status_code == 400
    assert response.json["message"] == "{'limit': ['Not a valid integer.']}"

    # offset
    # 200: response with a list of puzzles offseted by k place from the start
    # 400: offset must be 0 or above
    response = client.get('/puzzles?offset=-10')
    assert response.status_code == 400
    assert response.json["message"] == "{'offset': ['Must be 0 or above.']}"
    response = client.get('/puzzles?offset=apple')
    assert response.status_code == 400
    assert response.json["message"] == "{'offset': ['Not a valid integer.']}"

    # 400: sort_by must be either `id` or `difficulty`
    response = client.get('/puzzles?sort_by=name')
    assert response.status_code == 400
    assert response.json["message"] == "{'sort_by': ['Can only sort by either id or difficulty.']}"
    response = client.get('/puzzles?sort_by=100')
    assert response.status_code == 400
    assert response.json["message"] == "{'sort_by': ['Can only sort by either id or difficulty.']}"

    # 400: order must be either `asc` or `desc`
    response = client.get('/puzzles?order=ASC')
    assert response.status_code == 400
    assert response.json["message"] == "{'order': ['Can only accept order of asc or desc.']}"
    response = client.get('/puzzles?order=rev')
    assert response.status_code == 400
    assert response.json["message"] == "{'order': ['Can only accept order of asc or desc.']}"


def test_puzzles_get_by_id(client):
    # 200: should return with a single puzzle
    response = client.get('/puzzles/1')
    assert response.status_code == 200
    puzzle = response.json["puzzle"]
    assert puzzle["id"] == 1
    assert type(puzzle["puzzle"]) == str
    assert type(puzzle["solution"]) == str
    assert type(puzzle["score"]) == int
    assert type(puzzle["size"]) == str

    # 404: should return with not found error if no record for the given puzzle id
    response = client.get('/puzzles/9999999')
    assert response.status_code == 404
    response = client.get('/puzzles/invalid_id')
    assert response.status_code == 404
