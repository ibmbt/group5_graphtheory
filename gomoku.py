import os
os. system('cls')

BOARD_SIZE = 8
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


def count_in_direction(board, row, col, symbol, dx, dy):
    count = 0
    while 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == symbol:
        count += 1
        row += dx
        col += dy
    return count

def check_win(board, row, col, symbol):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in directions:
        total_count = (
            count_in_direction(board, row, col, symbol, dx, dy)
            + count_in_direction(board, row, col, symbol, -dx, -dy)
            - 1
        )
        if total_count >= WIN_CONDITION:
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


def minimax(board, depth, is_maximizing, alpha, beta, ai_symbol, human_symbol):
    # Check for terminal states
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] != '.':
                if check_win(board, row, col, ai_symbol):
                    return 10 - depth
                if check_win(board, row, col, human_symbol):
                    return depth - 10
    
    if not list_valid_moves(board):
        return 0

    if depth == 0:
        return evaluate_board(board, ai_symbol) - evaluate_board(board, human_symbol)

    if is_maximizing:
        max_eval = -float('inf')
        for row, col in list_valid_moves(board):
            board[row][col] = ai_symbol
            eval = minimax(board, depth - 1, False, alpha, beta, ai_symbol, human_symbol)
            board[row][col] = '.'
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for row, col in list_valid_moves(board):
            board[row][col] = human_symbol
            eval = minimax(board, depth - 1, True, alpha, beta, ai_symbol, human_symbol)
            board[row][col] = '.'
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
    
    
def is_threat(board, row, col, symbol):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dx, dy in directions:
        count = 0
        open_start = open_end = False


        x, y = row - dx, col - dy
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            if board[x][y] == symbol:
                count += 1
            elif board[x][y] == '.':
                open_start = True
                break
            else:
                break
            x -= dx
            y -= dy


        x, y = row + dx, col + dy
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            if board[x][y] == symbol:
                count += 1
            elif board[x][y] == '.':
                open_end = True
                break
            else:
                break
            x += dx
            y += dy


        if count == 3 and (open_start or open_end):
            return True

    return False



def ai_move(board, ai_symbol):
    human_symbol = 'O' if ai_symbol == 'X' else 'X'
    

    for row, col in list_valid_moves(board):
        board[row][col] = ai_symbol
        if check_win(board, row, col, ai_symbol):
            board[row][col] = '.'
            return row, col
        board[row][col] = '.' 
    

    for row, col in list_valid_moves(board):
        board[row][col] = human_symbol
        if check_win(board, row, col, human_symbol):
            board[row][col] = '.'
            return row, col
        board[row][col] = '.'

    
        for row, col in list_valid_moves(board):
            if is_threat(board, row, col, human_symbol):
                return row, col
        

    best_move = None
    best_score = -float('inf')
    
    for row, col in list_valid_moves(board):
        board[row][col] = ai_symbol
        move_score = minimax(
            board,
            depth=1,
            is_maximizing=False,
            alpha=-float('inf'),
            beta=float('inf'),
            ai_symbol=ai_symbol,
            human_symbol=human_symbol
        )
        board[row][col] = '.' 
        if move_score > best_score:
            best_score = move_score
            best_move = (row, col)
    
    if best_move:
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
