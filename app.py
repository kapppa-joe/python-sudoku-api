from sudoku_api import create_app, db

if __name__ == '__main__':
    app = create_app()
    app.run(threaded=True, port=5000)
