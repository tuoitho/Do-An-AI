from random import random
import tkinter as tk
import math


class TTT_GUI_PC(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tic Tac Toe')
        # self.geometry('650x750')
        self.configure(bg='#71BE38')

        self.char_x = tk.PhotoImage(file='images/x.png')
        self.char_o = tk.PhotoImage(file='images/o.png')
        self.empty = tk.PhotoImage()

        self.active = 'GAME ACTIVE'
        self.computer = {'win': 'COMPUTER WINS', 'image': self.char_o}
        self.user = {'win': 'USER WINS', 'image': self.char_x}
        self.board_bg = 'white'
        # nut reset

        self.reset_button = tk.Button(self, text='Reset', font=(
            'Helvetica', 14), command=self.reset, foreground='red', background='yellow', relief='raised', padx=109, pady=10)
        # show
        self.reset_button.grid(row=5, columnspan=3)

        # tạo board
        self.board = [[0]*3]*3
        self.remaining_moves = [[i, j] for i in range(3) for j in range(3)]
        self.state = self.active
        self.last_click = [0, 0]
        self.board_status = tk.StringVar()
        self.board_status.set(str(self.board))
        self.board_labels = []
        for i in range(3):
            row = []
            for j in range(3):
                label = tk.Label(self, highlightthickness=1,
                                 width=150, height=150, bg=self.board_bg,
                                 image=self.empty)
                label.grid(padx=5, pady=5)
                label.bind('<Button-1>',
                           lambda e, move=[i, j]: self.user_click(move))
                label.grid(row=i, column=j)
                row.append(label)
            self.board_labels.append(row)
        for i in range(3):
            for j in range(3):
                self.board_labels[i][j].bind(
                    '<Button-1>', lambda event, row=i, col=j: self.click(row, col))
        self.turn_label = tk.Label(
            self, text="Your turn", font=('Helvetica', 14))
        self.turn_label.grid(row=3, columnspan=3)
        self.HUMAN = -1
        self.COMP = +1
        # Khai báo hằng số

    def reset(self):
        self.board = [[0]*3]*3
        self.remaining_moves = [[i, j] for i in range(3) for j in range(3)]
        self.state = self.active
        self.last_click = [0, 0]
        self.board_status.set(str(self.board))
        self.turn_label.config(text="Your turn")
        for i in range(3):
            for j in range(3):
                self.board_labels[i][j].config(image=self.empty)
        # clear color of the winning row if it is colored
        for i in range(3):
            for j in range(3):
                self.board_labels[i][j].config(bg=self.board_bg)

    # Hàm đánh giá trạng thái
    def evaluate(self, state):
        if self.wins(state, self.COMP):
            score = +1
        elif self.wins(state, self.HUMAN):
            score = -1
        else:
            score = 0

        return score

    # Kiểm tra thắng thua
    def wins(self, state, player):
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
    def game_over(self, state):
        return self.wins(state, self.HUMAN) or self.wins(state, self.COMP)

    # Tìm ô trống
    def empty_cells(self, state):
        cells = []

        for x in range(3):
            for y in range(3):
                if state[x][y] == 0:
                    cells.append([x, y])

        return cells

    # Kiểm tra nước đi hợp lệ
    def valid_move(self, x, y):
        if [x, y] in self.empty_cells(self.board):
            return True
        else:
            return False

    # Đặt nước đi lên bàn cờ
    def set_move(self, x, y, player):
        if self.valid_move(x, y):
            self.board[x][y] = player
            return True
        else:
            return False

    def minimax(self, state, depth, player, alpha=-math.inf, beta=+math.inf):
        if player == self.COMP:
            best = [-1, -1, -math.inf]
        else:
            best = [-1, -1, math.inf]

        if depth == 0 or self.game_over(state):
            score = self.evaluate(state)
            return [-1, -1, score]

        for cell in self.empty_cells(state):
            x, y = cell[0], cell[1]
            state[x][y] = player

            score = self.minimax(state, depth - 1, self.HUMAN if player ==
                                 self.COMP else self.COMP, alpha, beta)
            if self.wins(state, self.COMP):
                state[x][y] = 0
                score[0], score[1] = x, y
                return score
            state[x][y] = 0
            score[0], score[1] = x, y

            if player == self.COMP:
                if score[2] > best[2]:
                    best = score
                alpha = max(alpha, score[2])
                if beta <= alpha:
                    break  # Beta cắt tỉa
            else:
                if score[2] < best[2]:
                    best = score
                beta = min(beta, score[2])
                if beta <= alpha:
                    break  # Alpha cắt tỉa
        return best

    # Hàm lượt đi của AI

    def ai_turn(self):
        print("ai turn")
        depth = len(self.empty_cells(self.board))
        print(depth)
        if depth == 9:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
        else:
            move = self.minimax(self.board, depth, self.COMP)
            x, y = move[0], move[1]

        self.set_move(x, y, self.COMP)
        self.board_status.set(str(self.board))

    def findwinrow(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
                return i
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
                return i+3
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return 6
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return 7
        return -1

    def click(self, row, col):
        if not self.game_over(self.board):
            self.board = eval(self.board_status.get())
            print(self.board, row, col)
            if self.valid_move(row, col):
                self.set_move(row, col, self.HUMAN)
                self.board_status.set(str(self.board))
                self.update_board()
                print("da click")
                if not self.game_over(self.board):
                    print("da click 2")
                    self.ai_turn()
                    self.update_board()

                if self.wins(self.board, self.COMP):
                    # coloring of the winning row
                    winrow = self.findwinrow()
                    if winrow < 3:
                        for i in range(3):
                            self.board_labels[winrow][i].config(bg='yellow')
                    elif winrow < 6:
                        for i in range(3):
                            self.board_labels[i][winrow-3].config(bg='yellow')
                    elif winrow == 6:
                        for i in range(3):
                            self.board_labels[i][i].config(bg='yellow')
                    else:
                        for i in range(3):
                            self.board_labels[i][2-i].config(bg='yellow')
                    self.turn_label.config(text="AI wins!")

                elif self.wins(self.board, self.HUMAN):
                    self.turn_label.config(text="You win!")
                elif len(self.empty_cells(self.board)) == 0:
                    self.turn_label.config(text="Draw!")

    def update_board(self):
        for i in range(3):
            for j in range(3):
                value = self.board[i][j]
                if value == 0:
                    self.board_labels[i][j].config(image=self.empty)
                elif value == self.HUMAN:
                    self.board_labels[i][j].config(image=self.char_x)
                else:
                    self.board_labels[i][j].config(image=self.char_o)


if __name__ == '__main__':
    root = TTT_GUI_PC()
    root.mainloop()
