# Sudoku API

A RESTful API microservice which currently provide two services:

1. Receive a sudoku puzzle and send back a solution.
2. Supply a list of sudoku puzzles with various difficulties rank.

The core of this program is a Sudoku solver / random puzzle generator written in python.

[Click here to see a running demo.](https://sudoku-solver-12345.herokuapp.com/api/)

---

## API Reference

### Sudoku puzzle solver

```http
  POST /api/solver
```

Format of request body:

| Parameter         | Type     | Description                                                                                                                                                    |
| :---------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `puzzle`          | `string` | **Required**. A string of 81 digits, which represent a Sudoku puzzle. Use `.` or `0` to denote empty cells.                                                    |
| `display_as_grid` | `bool`   | Optional. If set to true, the API will respond with a plain-text ASCII art of the Sudoku solution. Otherwise the solution will be a string. Default is `false` |

Example request body:

```json
{
  "puzzle": "000000270008270045040000008000567010005009007000040000200000401900010000650304792",
  "display_as_grid": "true"
}
```

Response:

```plaintext
+-------+-------+-------+
| 5 1 6 | 4 3 8 | 2 7 9 |
| 3 9 8 | 2 7 6 | 1 4 5 |
| 7 4 2 | 9 5 1 | 3 6 8 |
+-------+-------+-------+
| 8 2 3 | 5 6 7 | 9 1 4 |
| 4 6 5 | 1 2 9 | 8 3 7 |
| 1 7 9 | 8 4 3 | 5 2 6 |
+-------+-------+-------+
| 2 3 7 | 6 9 5 | 4 8 1 |
| 9 8 4 | 7 1 2 | 6 5 3 |
| 6 5 1 | 3 8 4 | 7 9 2 |
+-------+-------+-------+
```

Meaning of params in response body:

| Parameter              | Type     | Description                                                                                 |
| :--------------------- | :------- | :------------------------------------------------------------------------------------------ |
| `solution`             | `string` | A solution to the given Sudoku puzzle.                                                      |
| `alternative_solution` | `string` | An alternative solution to the given puzzle if there is more than one way to solve.         |
| `msg`                  | `string` | A message will be provided if your puzzle has more than 1 solution, or if it is unsolvable. |
|                        |

---

### Sudoku puzzle provider

```http
  GET /api/puzzles
```

| Parameter        | Type  | Description                                                                                                                        |
| :--------------- | :---- | :--------------------------------------------------------------------------------------------------------------------------------- |
| `min_difficulty` | `int` | The minimum difficulty of puzzles to retrieve. Refer the [related session](#about-difficulty-score) below for details              |
| `max_difficulty` | `int` | The maximam difficulty of puzzles to retrieve.                                                                                     |
| `size`           | `str` | _not implemented yet_ The size of the Sudoku puzzle. The common Sudoku puzzle with 9 digits is considered as `3x3` size.           |
| `sort_by`        | `str` | The value that puzzles are sorted. Currently supports `id` and `difficulty`                                                        |
| `order`          | `str` | To be used together with `sort_by` parameter. Supports `asc` for ascending order and `desc` for descending order. Default is `asc` |
| `limit`          | `int` | The maximum number of puzzles to retrieve in each request. Default is `10`                                                         |
| `offset`         | `int` | The number of records to skip before retrieviing the puzzle. Default is `0`                                                        |

Example queries:

| Description                                            | URL                                                   |
| :----------------------------------------------------- | :---------------------------------------------------- |
| Get the top 10 easiest puzzles in record               | `/api/puzzles?sort_by=difficulty&limit=10`            |
| Get the top 10 most difficult puzzles in record        | `/api/puzzles?sort_by=difficulty&order=desc&limit=10` |
| Get the #11~#20 puzzles in record, ordered by id       | `/api/puzzles?sort_by=id&limit=10&offset=10`          |
| Get only puzzles with difficuly scores higher than 200 | `/api/puzzles?min_difficulty=200`                     |

### About difficulty score

The difficulty score of puzzles are computed with the algorithm described in [this article](https://dlbeer.co.nz/articles/sudoku.html).

Generally speaking, puzzles with difficulty score < 100 are usually easy to solve, and puzzles with difficulty score > 300 are considered challenging.

## Installation / Run Locally

This project is tested to work with:

- Python version: (3.10.0) [Download Python](https://www.python.org/downloads/)
- pip version: (21.3.1)
- Flask version: (2.0.2)

**Note:**
It might be a good idea to setup an environment management system before installing on your local machine.

Various options are available, such as [venv](https://docs.python.org/3/tutorial/venv.html), [conda](https://docs.conda.io/en/latest/) or [mamba](https://github.com/mamba-org/mamba).

(I used mamba when I developed this software.)

After you have setup your virtual environment, follow these steps to run this project locally:

Clone the project

```bash
  git clone https://github.com/kapppa-joe/python-sudoku-api
```

Go to the project directory

```bash
  cd python-sudoku-api
```

Install the dependencies with below command:

```bash
  pip install -r requirements.txt
```

Start the server:

```bash
  flask run
```

Then visit `localhost:5000` to access the server at your local machine.

---

## Credit / Acknowledgements

- Thanks to Daniel Beer for his [awesome article on how to generate Sudoku puzzles](https://dlbeer.co.nz/articles/sudoku.html). The Sudoku puzzle generating algorithm I used is very much inspired by his work.

- Thanks to Miguel Grinberg for this [great tutorial on setting up a Flask project](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

- README file was generated by [readme.so](https://readme.so)

---

## License

[MIT](https://choosealicense.com/licenses/mit/)
