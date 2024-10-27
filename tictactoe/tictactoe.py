from random import choice
from math import inf as infinity

X = "X"
O = "O"
EMPTY = None

# Define these globally
pl = X
first = True

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    global pl, first
    no_of_x = sum(row.count(X) for row in board)
    no_of_o = sum(row.count(O) for row in board)

    if first:
        first = False
        return pl
    elif no_of_x > no_of_o:
        pl = O
    else:
        pl = X

    return pl

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return [(x, y) for x, row in enumerate(board) for y, cell in enumerate(row) if cell == EMPTY]

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = [row[:] for row in board]
    x, y = action
    new_board[x][y] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win_state = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]],
    ]
    if [X, X, X] in win_state:
        return X
    elif [O, O, O] in win_state:
        return O
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or not any(EMPTY in row for row in board)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def ai_turn(board, length, current_pl):
    """
    Implements the Minimax algorithm to find the best move in the game.
    """

    if current_pl == X:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if length == 0 or terminal(board):
        score = utility(board)
        return [-1, -1, score]

    for cell in actions(board):
        x, y = cell
        new_board = result(board, (x, y))
        score = ai_turn(new_board, length - 1, player(new_board))
        score[0], score[1] = x, y

        if current_pl == X:
            if score[2] > best[2]:
                best = score  # Max value
        else:
            if score[2] < best[2]:
                best = score  # Min value

    return best

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    length = len(actions(board))
    if length == 0 or terminal(board):
        return None

    if length == 9:
        return choice([(0, 0), (0, 2), (2, 0), (2, 2)])
    else:
        move = ai_turn(board, length, player(board))
        return move[0], move[1]
