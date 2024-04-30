from random import random
import tkinter as tk
import math

# Khai báo hằng số
HUMAN = -1
COMP = +1

# Hàm đánh giá trạng thái
def evaluate(state):
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score

# Kiểm tra thắng thua
def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]

    if [player, player, player] in win_state:
        return True
    else:
        return False

# Kiểm tra hết nước đi
def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)

# Tìm ô trống
def empty_cells(state):
    cells = []

    for x in range(3):
        for y in range(3):
            if state[x][y] == 0:
                cells.append([x, y])

    return cells

# Kiểm tra nước đi hợp lệ
def valid_move(x, y):
    if [x, y] in empty_cells(board):
        return True
    else:
        return False

# Đặt nước đi lên bàn cờ
def set_move(x, y, player):
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False

# Thuật toán Minimax
def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -math.inf]
    else:
        best = [-1, -1, math.inf]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best

# Hàm lượt đi của AI
def ai_turn():
    depth = len(empty_cells(board))
    if depth == 9:
        x = random.randint(0, 2)
        y = random.randint(0, 2)
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    board_status.set(str(board))

# Giao diện với Tkinter
root = tk.Tk()
root.title("Tic Tac Toe - Minimax")

board_status = tk.StringVar()
board_status.set(str([
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]))

board_labels = []
for i in range(3):
    row = []
    for j in range(3):
        label = tk.Label(root, text=' ', font=('Helvetica', 32), width=3, height=1, bg='white', relief='sunken')
        label.grid(row=i, column=j)
        row.append(label)
    board_labels.append(row)

turn_label = tk.Label(root, text="Your turn", font=('Helvetica', 14))
turn_label.grid(row=3, columnspan=3)

def click(row, col):
    global board
    board = eval(board_status.get())

    if valid_move(row, col):
        set_move(row, col, HUMAN)
        board_status.set(str(board))
        update_board()

        if not game_over(board):
            ai_turn()
            update_board()

        if wins(board, COMP):
            turn_label.config(text="AI wins!")
        elif wins(board, HUMAN):
            turn_label.config(text="You win!")
        elif len(empty_cells(board)) == 0:
            turn_label.config(text="Draw!")

def update_board():
    board = eval(board_status.get())
    for i in range(3):
        for j in range(3):
            value = board[i][j]
            if value == 0:
                board_labels[i][j].config(text=' ')
            elif value == HUMAN:
                board_labels[i][j].config(text='X')
            else:
                board_labels[i][j].config(text='O')

for i in range(3):
    for j in range(3):
        board_labels[i][j].bind('<Button-1>', lambda event, row=i, col=j: click(row, col))

root.mainloop()