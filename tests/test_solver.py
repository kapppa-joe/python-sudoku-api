def test_solver_get(client):
    # 200: return a msg to tell user to POST a puzzle
    response = client.get('/solver')
    assert response.status_code == 200
    assert response.json["msg"] == "POST a Sudoku puzzle to this url and I will solve it for you! :)"


def test_solver_post(client):
    # 400: POST request without body
    response = client.post('/solver')
    assert response.status_code == 400
    assert response.json["msg"] == r"sorry, only accept a body with format {puzzle: str}, where str is a string of 81 digits representing a Sudoku puzzle"

    # 400: POST request with empty body
    response = client.post('/solver', data="")
    assert response.status_code == 400
    assert response.json["msg"] == r"sorry, only accept a body with format {puzzle: str}, where str is a string of 81 digits representing a Sudoku puzzle"

    # 200: for a valid puzzle body, return with the solution
    valid_puzzle = '000000270008270045040000008000567010005009007000040000200000401900010000650304792'
    response = client.post('/solver', data={"puzzle": valid_puzzle})
    assert response.status_code == 200
    assert response.json["solution"] == '516438279398276145742951368823567914465129837179843526237695481984712653651384792'

    # 200: for a valid puzzle with more than 1 solution, return 2 solutions and a msg
    valid_puzzle_multi_sulution = "123456789" + '.' * 72
    response = client.post(
        '/solver', data={"puzzle": valid_puzzle_multi_sulution})
    assert response.status_code == 200
    assert response.json["solution"] == '123456789456789123789123456231674895875912364694538217317265948542897631968341572'
    assert response.json["msg"] == "more than 1 solution found for given puzzle. only returning the first two solutions found."
    assert response.json["alternative_solution"].startswith('123456789')

    # 400: for an unsolvable puzzle, return with an error msg
    unsolvable_puzzle = "516849732307605000809700065135060907472591006968370050253186074684207500791050608"
    response = client.post('/solver', data={"puzzle": unsolvable_puzzle})
    assert response.status_code == 400
    assert response.json['msg'] == 'puzzle is unsolvable'

    # 400: for an invalid puzzle, return with an error msg
    test_cases = [
        '0' * 80,  # length_too_short
        '0' * 82,  # length_too_long
        'A23456789' + '0' * 72,  # invalid_char
        '113456789' + '0' * 72,  # duplicate_number_in_row
        '1234567891' + '0' * 71,  # duplicate_number_in_column
        '1234567892' + '0' * 71  # duplicate_number_in_square
    ]

    for invalid_puzzle in test_cases:
        response = client.post('/solver', data={"puzzle": invalid_puzzle})
        assert response.status_code == 400
