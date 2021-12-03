# This file should contain records you want created when you run flask db seed.
#
# Example:
# from yourapp.models import User


from sudoku_api.models.Puzzle import Puzzle
from sudoku_api.core import Sudoku


# initial_user = {
#     'username': 'superadmin'
# }
# if User.find_by_username(initial_user['username']) is None:
#     User(**initial_user).save()
