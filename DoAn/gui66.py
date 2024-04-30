import tkinter as tk
from math import inf as infinity
from random import choice

HUMAN = -1
COMP = +1

def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    This function tests if a specific player wins. Possibilities:
    * Three rows    [X X X] or [O O O]
    * Three cols    [X X X] or [O O O]
    * Two diagonals [X X X] or [O O O]
    :param state: the state of the current board
    :param player: a human or a computer
    :return: True if the player wins
    """
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


def game_over(state):
    """
    This function test if the human or computer wins
    :param state: the state of the current board
    :return: True if the human or computer wins
    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


# def valid_move(x, y):
#     """
#     A move is valid if the chosen cell is empty
#     :param x: X coordinate
#     :param y: Y coordinate
#     :return: True if the board[x][y] is empty
#     """
#     if [x, y] in empty_cells(board):
#         return True
#     else:
#         return False


# def set_move(x, y, player):
#     """
#     Set the move on board, if the coordinates are valid
#     :param x: X coordinate
#     :param y: Y coordinate
#     :param player: the current player
#     """
#     if valid_move(x, y):
#         board[x][y] = player
#         return True
#     else:
#         return False


def minimax(state, depth, player):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an human or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

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
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def render(state, c_choice, h_choice):
    """
    Print the board on console
    :param state: current state of the board
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


# def ai_turn(c_choice, h_choice):
#     """
#     It calls the minimax function if the depth < 9,
#     else it choices a random coordinate.
#     :param c_choice: computer's choice X or O
#     :param h_choice: human's choice X or O
#     :return:
#     """
#     depth = len(empty_cells(board))
#     if depth == 0 or game_over(board):
#         return

#     print(f'Computer turn [{c_choice}]')
#     render(board, c_choice, h_choice)

#     if depth == 9:
#         x = choice([0, 1, 2])
#         y = choice([0, 1, 2])
#     else:
#         move = minimax(board, depth, COMP)
#         x, y = move[0], move[1]

#     set_move(x, y, COMP)


# def human_turn(c_choice, h_choice):
#     """
#     The Human plays choosing a valid move.
#     :param c_choice: computer's choice X or O
#     :param h_choice: human's choice X or O
#     :return:
#     """
#     depth = len(empty_cells(board))
#     if depth == 0 or game_over(board):
#         return

#     # Dictionary of valid moves
#     move = -1
#     moves = {
#         1: [0, 0], 2: [0, 1], 3: [0, 2],
#         4: [1, 0], 5: [1, 1], 6: [1, 2],
#         7: [2, 0], 8: [2, 1], 9: [2, 2],
#     }

#     print(f'Human turn [{h_choice}]')
#     render(board, c_choice, h_choice)

#     while move < 1 or move > 9:
#         try:
#             move = int(input('Use numpad (1..9): '))
#             coord = moves[move]
#             can_move = set_move(coord[0], coord[1], HUMAN)

#             if not can_move:
#                 print('Bad move')
#                 move = -1
#         except (EOFError, KeyboardInterrupt):
#             print('Bye')
#             exit()
#         except (KeyError, ValueError):
#             print('Bad choice')


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tic Tac Toe')
        self.geometry('700x700')

        self.char_x = tk.PhotoImage(file='x.png')
        self.char_o = tk.PhotoImage(file='o.png')
        self.empty = tk.PhotoImage()

        self.active = 'GAME ACTIVE'
        self.line_size = 3
        self.computer = {'value': 1, 'bg': 'orange',
                         'win': 'COMPUTER WINS', 'image': self.char_o}
        self.user = {'value': self.line_size+1, 'bg': 'grey',
                     'win': 'USER WINS', 'image': self.char_x}
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_radio_frame()
        self.create_control_frame()

    def create_radio_frame(self):
        self.radio_frame = tk.Frame()
        self.radio_frame.pack(side=tk.TOP, pady=5)

        tk.Label(self.radio_frame, text='First Move').pack(side=tk.LEFT)
        self.radio_choice = tk.IntVar()
        self.radio_choice.set(self.user['value'])
        tk.Radiobutton(self.radio_frame, text='Computer',
                       variable=self.radio_choice, value=self.computer['value']
                       ).pack(side=tk.LEFT)
        tk.Radiobutton(self.radio_frame, text='User',
                       variable=self.radio_choice, value=self.user['value']
                       ).pack(side=tk.RIGHT)

    def create_control_frame(self):
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP, pady=5)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.LEFT)

        self.b_play = tk.Button(self.control_frame, text='Play',
                                command=self.play)
        self.b_play.pack(side=tk.RIGHT)

    def create_status_frame(self):
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True)

        tk.Label(self.status_frame, text='Status: ').pack(side=tk.LEFT)
        self.l_status = tk.Label(self.status_frame)
        self.l_status.pack(side=tk.RIGHT)

    def create_board_frame(self):
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        # self.cell = [None] * self.total_cells
        self.cell = [[None]*3]*3
        # self.board = [0] * self.total_cells
        self.board = [[0]*3]*3

        self.remaining_moves = [[i,j] for i in range(3) for j in range(3)]
        # self.remaining_moves = list(range(self.total_cells))
        
        # for i in range(self.total_cells):
        #     self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,
        #                             width=200, height=200, bg=self.board_bg,
        #                             image=self.empty)
        #     # margin
        #     self.cell[i].grid(padx=5, pady=5)
        #     self.cell[i].bind('<Button-1>',
        #                       lambda e, move=i: self.user_click(e, move))
        #     r, c = divmod(i, self.line_size)
        #     self.cell[i].grid(row=r, column=c)
        def user_click(user_move):
                # print(2)
                print(user_move[0],user_move[1])
                # print(self.board)
                if self.board[user_move[0]][user_move[1]] != 0 or self.state != self.active:
                    return
                self.update_board(self.user, user_move)
                # if self.state == self.active:
                #     self.computer_click()
        for i in range(3):
            for j in range(3):
                self.cell[i][j] = tk.Label(self.board_frame, highlightthickness=1,
                                           width=200, height=200, bg=self.board_bg,
                                           image=self.empty)
                # margin
                self.cell[i][j].grid(padx=5, pady=5)
                # self.cell[i][j].bind('<Button-1>',lambda e, move=[i,j]: print(move))
                self.cell[i][j].bind('<Button-1>',
                                     lambda e,move=[i, j]: user_click(move))
                self.cell[i][j].grid(row=i, column=j)

    def play(self):
        self.b_play['state'] = 'disabled'
        if self.b_play['text'] == 'Play':
            self.create_status_frame()
            self.b_play['text'] = 'Play Again'
        else:
            self.board_frame.destroy()
        self.l_status['text'] = self.active
        self.state = self.active
        # self.last_click = 0
        self.last_click = [0,0]
        self.create_board_frame()
        if self.radio_choice.get() == self.computer['value']:
            self.computer_click()

    def quit(self):
        self.destroy()

    
    # def user_click(self, e, user_move):
    #     if self.board[user_move] != 0 or self.state != self.active:
    #         return
    #     self.update_board(self.user, user_move)
    #     if self.state == self.active:
    #         self.computer_click()

    # def computer_click(self):
    #     computer_move = random.choice(self.remaining_moves)
    #     self.update_board(self.computer, computer_move)
    def computer_click(self):
        move = minimax(self.board, len(empty_cells(self.board)), COMP)
        self.update_board(self.computer, move[0] * self.line_size + move[1])

    def update_board(self, player, move):
        print(move[0],move[1])
        self.board[move[0]][move[1]] = player['value']
        print(move[0],move[1])
        self.remaining_moves.remove(move)
        print("dd")
        # self.cell[self.last_click[0]][self.last_click[1]]['bg'] = self.board_bg
        print("d2")
        self.last_click = move
        self.cell[move[0]][move[1]]['image'] = player['image']
        self.cell[move[0]][move[1]]['bg'] = player['bg']
        self.update_status(player)
        self.l_status['text'] = self.state
        if self.state != self.active:
            self.b_play['state'] = 'normal'
    # def update_board(self, player, move):
    #     self.board[move] = player['value']
    #     self.remaining_moves.remove(move)
    #     self.cell[self.last_click]['bg'] = self.board_bg
    #     self.last_click = move
    #     self.cell[move]['image'] = player['image']
    #     self.cell[move]['bg'] = player['bg']
    #     self.update_status(player)
    #     self.l_status['text'] = self.state
    #     if self.state != self.active:
    #         self.b_play['state'] = 'normal'

    def update_status(self, player):
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.state = player['win']
                self.highlight_winning_line(player, line)
        if self.state == self.active and not self.remaining_moves:
            self.state = 'TIE'

    def highlight_winning_line(self, player, line):
        for i in line:
            self.cell[i]['bg'] = player['bg']


if __name__ == '__main__':
    root = Root()
    root.mainloop()
