from sudoku_api import app, db

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
