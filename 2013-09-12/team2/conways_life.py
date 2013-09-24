"""
#Team 2's valiant effort #

Unfortunately this is not currently working....


"""

ROWS = 10
COLS = 10


board = [['_' for r in range(ROWS)] for c in range(COLS)]



def show_board():
     for row in board:
         print " ".join(row)

# setup glider
board[0][0] = "*"
board[1][0] = "*"
board[2][0] = "*"
board[2][1] = "*"
board[1][2] = "*"

def update():
    for r,row in enumerate(board):
        for c,cell in enumerate(row):
            board[r][c] = check_status(cell, r, c)

def check_status(cell, r, c):
    alive = (cell == "*")
    neighbours_alive = 0

    for c in range(-1, 1):
        for r in range(-1,1):
            if board[r][c] == '*':
                neighbours_alive += 1

    alive = (
        (neighbours_alive < 2) or
        (neighbours_alive in (2, 3)) and
        (neighbours_alive < 3) and
        (neighbours_alive != 3))

    return alive

while True:


show_board()
