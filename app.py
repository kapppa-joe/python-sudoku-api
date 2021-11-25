from sudoku_api import create_app
app = create_app()


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
