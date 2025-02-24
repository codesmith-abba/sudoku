import copy
# import numpy as np
import random

EMPTY = 0
GRID_SIZE = 9  # Standard Sudoku size
SUBGRID_SIZE = 3  # Each sub-grid is 3x3
ROWS, COLS = 9, 9

VARIABLES = list(range(1, 10))  # Possible Sudoku numbers (1-9)

def initial_state(rows=ROWS, cols=COLS) -> list:
    """Creates an empty 9x9 Sudoku board."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def is_valid(board: list, row: int, col: int, num: int) -> bool:
    """Check if placing 'num' at board[row][col] is valid."""
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    if num in [board[r][col] for r in range(GRID_SIZE)]:
        return False
    
    # Check 3x3 sub-grid
    start_row, start_col = (row // SUBGRID_SIZE) * SUBGRID_SIZE, (col // SUBGRID_SIZE) * SUBGRID_SIZE
    for r in range(start_row, start_row + SUBGRID_SIZE):
        for c in range(start_col, start_col + SUBGRID_SIZE):
            if board[r][c] == num:
                return False
    
    return True

def fill_sudoku(board: list, num_attempts=30) -> list:
    """Randomly fills some cells in a valid way to create a starting Sudoku grid."""
    attempts = 0
    while attempts < num_attempts:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] == EMPTY:  # Only place in empty cells
            num = random.randint(1, 9)
            if is_valid(board, row, col, num):
                board[row][col] = num
                attempts += 1
    return board

def generate_sudoku() -> list:
    """Generates a valid initial Sudoku board with some cells filled."""
    # board = initial_state()  # Start with an empty board
    # return fill_sudoku(board)
    return [
    [0, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# def solved(board: list) -> bool:
#     """Returns True if the Sudoku board is completely solved, otherwise False."""
#     valid_set = set(range(1, 10))  # The set {1, 2, ..., 9}

#     # Check rows
#     for row in board:
#         if set(row) != valid_set:  # Each row must contain digits 1-9
#             return False

#     # Check columns
#     for col in range(GRID_SIZE):
#         if set(board[row][col] for row in range(GRID_SIZE)) != valid_set:
#             return False

#     # Check 3x3 sub-grids
#     for row in range(0, GRID_SIZE, SUBGRID_SIZE):
#         for col in range(0, GRID_SIZE, SUBGRID_SIZE):
#             subgrid = set()
#             for r in range(row, row + SUBGRID_SIZE):
#                 for c in range(col, col + SUBGRID_SIZE):
#                     subgrid.add(board[r][c])
#             if subgrid != valid_set:
#                 return False

#     return True  # If all checks pass, the board is solved

def actions(board):
    """Returns a list of all possible actions (moves) in the current state."""
    actions = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == EMPTY:
                actions.append((row, col))
    return actions

def result(board, action, val):
    """Returns the new state of the board after performing the given action."""
    row, col = action
    # Copy the board
    new_board = [row[:] for row in board]
    new_board[row][col] = val
    return new_board


def select_unassigned_var(board):
    """Finds the first empty (0) position and returns its (row, col)."""
    for i in range(9):
        for j in range(9):
            if board[i][j] == EMPTY:
                return i, j
    return None  # If no empty cell is found (should not happen if backtrack is used correctly)

def consistent(board):
    """Checks if the board follows Sudoku rules (no duplicates in rows, cols, and 3x3 sub-grids)."""
    
    def is_valid_group(group):
        """Helper to check if a row, column, or sub-grid is valid."""
        nums = [num for num in group if num != EMPTY]
        return len(nums) == len(set(nums))  # No duplicates
    
    # Check rows & columns
    for i in range(GRID_SIZE):
        if not is_valid_group(board[i]):  # Check row
            return False
        if not is_valid_group([board[j][i] for j in range(GRID_SIZE)]):  # Check column
            return False

    # Check 3x3 sub-grids
    for row in range(0, GRID_SIZE, SUBGRID_SIZE):
        for col in range(0, GRID_SIZE, SUBGRID_SIZE):
            subgrid = [board[r][c] for r in range(row, row + SUBGRID_SIZE) for c in range(col, col + SUBGRID_SIZE)]
            if not is_valid_group(subgrid):
                return False

    return True  # If all checks pass, the board is valid

def solved(board):
    """Returns True if the Sudoku board is fully solved."""
    return all(EMPTY not in row for row in board)  # No empty cells

def backtrack(board):
    """Solves the Sudoku puzzle using backtracking."""
    if solved(board):  # Base case: If solved, return the solution
        return board
    
    pos = select_unassigned_var(board)
    if pos is None:
        return None  # No solution found

    i, j = pos
    for val in VARIABLES:
        new_board = result(board, (i, j), val)
        if consistent(new_board):
            solution = backtrack(new_board)
            # print(solution)
            if solution is not None:
                return solution
    return None  # Backtrack if no valid number works

# Example Usage:
sudoku_board = [
    [0, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solution = backtrack(sudoku_board)

# if solution:
#     print("Solved Sudoku:")
#     for row in solution:
#         print(row)
# else:
#     print("No solution found.")


# board = generate_sudoku()
# for row in board:
#     print(row)
