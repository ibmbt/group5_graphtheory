BOARD_SIZE = 5
WIN_CONDITION = 5


def initialize_board(size):
    board = []
    for _ in range(size):
        row = ['.'] * size
        board.append(row)
    return board


def display_board(board):
    for row in board:
        print(' '.join(row))
    print()


def is_move_valid(board, row, col):
    is_row_valid = (row >= 0 and row < BOARD_SIZE)
    is_col_valid = (col >= 0 and col < BOARD_SIZE)
    is_cell_empty = (board[row][col] == '.')
    return is_row_valid and is_col_valid and is_cell_empty


def check_direction(board, row, col, symbol, dx, dy, count):

    if count >= WIN_CONDITION:
        return True

    new_row = row + dx
    new_col = col + dy

    if (0 <= new_row < BOARD_SIZE) and (0 <= new_col < BOARD_SIZE):
        if board[new_row][new_col] == symbol:
            return check_direction(board, new_row, new_col, symbol, dx, dy, count + 1)

    return False


def check_win(board, row, col, symbol):
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    for dx, dy in directions:
        count = 1

        if check_direction(board, row, col, symbol, dx, dy, count):
            return True

        if check_direction(board, row, col, symbol, -dx, -dy, count):
            return True

    return False

