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


def player_move(board, symbol):
    while True:
        row, col = map(int, input("Enter row and column: ").split())
        if is_move_valid(board, row, col):
            board[row][col] = symbol
            return row, col
        else:
            print("Invalid move. Try again.")


def player2_move(board, symbol):
    while True:
        row, col = map(int, input("Enter row and column: ").split())
        if is_move_valid(board, row, col):
            board[row][col] = symbol
            return row, col
        else:
            print("Invalid move. Try again.")


def list_valid_moves(board):
    return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] == '.']


def evaluate_board(board, symbol):
    score = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == symbol:
                queue = [(row, col)]
                visited = set(queue)
                while queue:
                    x, y = queue.pop(0)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                            if board[nx][ny] == '.':
                                score = score + 1
                            elif board[nx][ny] == symbol and (nx, ny) not in visited:
                                visited.add((nx, ny))
                                queue.append((nx, ny))
    return score


# (need more checks for higher difficulty)
def ai_move(board, symbol):
    best_move = None
    best_score = -float('inf')
    for move in list_valid_moves(board):
        row, col = move
        board[row][col] = symbol
        score = evaluate_board(board, symbol)
        board[row][col] = '.'
        if score > best_score:
            best_score = score
            best_move = (row, col)
    return best_move


def play_game():
    board = initialize_board(BOARD_SIZE)
    current_player = "TahirBhai"
    ai_symbol = 'X'
    human2_symbol = 'X'
    human_symbol = 'O'

    display_board(board)

    while True:
        if current_player == "TahirBhai":
            print("Your turn:")
            row, col = player_move(board, human_symbol)
            if check_win(board, row, col, human_symbol):
                display_board(board)
                print("TahirBhai wins!")
                break
            current_player = "AI"
            # current_player = "human_2"
        else:
            print("AI's turn:")
            # print("player2's turn:")
            # row, col = player2_move(board, human_symbol)
            row, col = ai_move(board, ai_symbol)
            if row is not None and col is not None:
                board[row][col] = ai_symbol
                # board[row][col] = human2_symbol
                if check_win(board, row, col, ai_symbol):
                    display_board(board)
                    print("AI wins!")
                    #print("player2 wins!")
                    break
            current_player = "TahirBhai"

        display_board(board)

        if not list_valid_moves(board):
            print("It's a draw!")
            break


play_game()
