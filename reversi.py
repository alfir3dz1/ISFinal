#Referenced from Winston Liu
import itertools
from copy import deepcopy


def newboard(size):
    board = [[' ' for y in range(size)] for x in range(size)]
    c = size // 2
    board[c - 1][c - 1] = 'O'
    board[c - 1][c] = 'X'
    board[c][c - 1] = 'X'
    board[c][c] = 'O'
    return board


def draw(board):
    for row in range(len(board)):
        print("+-" * len(board) + "+")
        for col in range(len(board[row])):
            c = board[col][row]
            print("|" + c, end='')
        print("|")
    print("+-" * len(board) + "+")


def drawmove(board, player):
    moves = movablemoves(board, player)
    for row in range(len(board)):
        print("+---" * len(board) + "+")
        for col in range(len(board[row])):
            c = board[col][row]
            c = '.' if (col, row) in moves else c
            print("| " + c, end=' ')
        print("|")
    print("+---" * len(board) + "+")


def computer(player):
    return 'X' if player == 'O' else 'O' if player == 'X' else None


def movablemoves(board, player, prev_passed=False):
    board_size = len(board)
    AI = computer(player)
    moves = []
    for x, y in itertools.product(range(board_size), range(board_size)):
        if board[x][y] != ' ':
            continue
        for dx, dy in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            x_ = x
            y_ = y
            valid_move_found = False
            found_AI = False
            while True:
                x_ += dx
                y_ += dy
                if x_ < 0 or x_ >= board_size or y_ < 0 or y_ >= board_size:
                    break
                elif board[x_][y_] == AI:
                    found_AI = True
                elif found_AI and board[x_][y_] == player:
                    moves.append((x, y))
                    valid_move_found = True
                    break
                elif board[x_][y_] == ' ' or board[x_][y_] == player:
                    break
            if valid_move_found:
                break
    if len(moves) == 0 and not prev_passed and len(movablemoves(board, AI, prev_passed=True)) > 0:
        return [None]
    return moves


def make_move(board, move, player):
    if move is None:
        return

    x, y = move

    board_size = len(board)
    board[x][y] = player
    AI = computer(player)
    for dx, dy in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
        x_ = x
        y_ = y
        found_AI = False
        while True:
            x_ += dx
            y_ += dy
            if x_ < 0 or x_ >= board_size or y_ < 0 or y_ >= board_size:
                break
            elif board[x_][y_] == AI:
                found_AI = True
            elif found_AI and board[x_][y_] == player:
                while x_ != x or y_ != y:
                    board[x_][y_] = player
                    x_ -= dx
                    y_ -= dy
                break
            elif board[x_][y_] == ' ' or board[x_][y_] == player:
                break
    return


def scoreboard(board):

    score = 0
    for row in board:
        for c in row:
            if c == 'X':
                score += 1
            elif c == 'O':
                score -= 1
    return score


def get_score(board):

    xs = 0
    os = 0
    for row in board:
        for c in row:
            if c == 'X':
                xs += 1
            elif c == 'O':
                os += 1
    return {'X': xs, 'O': os}


if __name__ == '__main__':
    board = newboard(4)
    drawmove(board, 'X')
    make_move(board, (1, 0), 'X')
    drawmove(board, 'O')
    make_move(board, (2, 0), 'O')
    drawmove(board, 'X')
    make_move(board, (3, 2), 'X')
    drawmove(board, 'O')

    print('end')
