from sudoku_api.core import Sudoku

sudoku = Sudoku()


def test_puzzles_get(client):
    # 200: return with a random sudoku puzzles
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
