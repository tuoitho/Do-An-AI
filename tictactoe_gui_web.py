from math import inf as infinity
from random import choice
import base64
import numpy as np
import streamlit as st
from streamlit.components.v1 import html

HUMAN = '❌'
COMP = '⭕'
EMPTY_CELL = ' '

st.sidebar.markdown(
    """
    <div class="red-text">
        Chào mừng đến với dự án của chúng tôi
         <p><b style="font-size: 40px;">Personal Information:</b></p>
        <div>
    Student 1: </p>
        Full name: Lê Đình Trí</p>
        ID: 22110442 </p>
    Student 2:</p>
        Full name: Liên Huệ Tiên</p>
        ID: 22110433 </p>
    School name: HCM University of Technology and Education
        </div>
	<p><b style="font-size: 40px;">Contact me:</b></p>
	<div>
        <p>Github: <a style="color:green" href=https://github.com/iamtien-cmd>https://github.com/iamtien-cmd</a></p>
        <p>Facebook:<a style="color:green" href=https://www.facebook.com/profile.php?id=100086303203036> https://www.facebook.com/profile.php?id=100086303203036</a></p>
        <p>Email: <a style="color:green" href="">22110433@student.hcmute.edu.vn</a></p>
        <p>Phone: <a style="color:green" href=""> 0865057353</a></p>
	</div>
 <div>
        <p>Github: <a style="color:green" href=https://github.com/tuoitho/>https://github.com/tuoitho/</a></p>
        <p>Facebook:<a style="color:green" href=https://www.facebook.com/tuoithodakhoc/> https://www.facebook.com/tuoithodakhoc/</a></p>
        <p>Email: <a style="color:green" href="">22110442@student.hcmute.edu.vn</a></p>
        <p>Phone: <a style="color:green" href="">0362092749></a></p>
	</div>
	<p><b style="font-size: 40px;">Instructor Information:</b></p>
   	<div>
        <p>- Teacher: Tran Tien Duc</p>
        <p>- Email:<a style="color:green" href="ductt@hcmute.edu.vn"> ductt@hcmute.edu.vn</a></p>
	</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #f9e9d6;
    }
</style>
""", unsafe_allow_html=True)

def init(post_init=False):
    st.balloons()
    st.session_state.win = {HUMAN: 0, COMP: 0}
    st.session_state.board = np.full((3, 3), EMPTY_CELL, dtype=str)
    st.session_state.player = HUMAN
    st.session_state.warning = False
    st.session_state.winner = None
    st.session_state.over = False
    
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('images/bg.jpg')

def check_state():
    if st.session_state.winner:
        st.success(f"Congrats! {st.session_state.winner} won the game! 🎈")
        st.balloons()
        st.balloons()
        st.balloons()

    if st.session_state.warning and not st.session_state.over:
        st.warning('⚠️ This move already exist')
    if st.session_state.winner and not st.session_state.over:
        st.session_state.over = True
        st.session_state.win[st.session_state.winner] = (
            st.session_state.win.get(st.session_state.winner, 0) + 1
        )
    elif not empty_cells(st.session_state.board) and not st.session_state.winner:
        st.info(f'It\'s a tie 📍')
        st.session_state.over = True


def computer_player():
    depth = len(empty_cells(st.session_state.board))
    if depth == 0 or game_over(st.session_state.board):
        return
    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(st.session_state.board, depth, COMP)
        x, y = move[0], move[1]
        handle_click(x, y)


def handle_click(i, j):
    if [i, j] not in empty_cells(st.session_state.board):
        st.session_state.warning = True
    elif not st.session_state.winner:
        st.session_state.warning = False
        st.session_state.board[i, j] = str(st.session_state.player)
        st.session_state.player = COMP if st.session_state.player == HUMAN else HUMAN
        winner = HUMAN if wins(st.session_state.board, HUMAN) else COMP if wins(
            st.session_state.board, COMP) else None
        if winner != None:
            st.session_state.winner = winner


button_style = """
        <style>
        .stButton > button {
            color: black;
            width: 90px;
            height: 90px;
            font-size: 20px;
            border-radius:10px;
            padding: 20px;
        }
        </style>
        """
st.markdown(button_style, unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .stSessionState {
        background-color: #173;
    }
    </style>
    """,
    unsafe_allow_html=True
)


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
#


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
            if cell == EMPTY_CELL:
                cells.append([x, y])
    return cells


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



def minimax(state, depth, player, alpha=-infinity, beta=+infinity):
    # AI function that chooses the best move.
    row, col = -1, -1
    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [row, col, score]
    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, HUMAN if player ==
                        COMP else COMP, alpha, beta)
        if wins(state,COMP):
            state[x][y] =' '
            score[0],score[1]=x,y
            return score
        state[x][y] = EMPTY_CELL
        if player == COMP:
            if score[2] > alpha:
                row = x
                col = y
            alpha = max(alpha, score[2])
            if beta <= alpha:
                break  # Beta cắt tỉa
        else:
            if score[2] < beta:
                row = x
                col = y
            beta = min(beta, score[2])
            if beta <= alpha:
                break  # Alpha cắt tỉa
        if alpha >= beta:
            break

    if player == COMP:
        return [row, col, alpha]
    else:
        return [row, col, beta]
# def minimax(state, depth, player):
#     """
#     AI function that choice the best move
#     :param state: current state of the board
#     :param depth: node index in the tree (0 <= depth <= 9),
#     but never nine in this case (see iaturn() function)
#     :param player: an human or a computer
#     :return: a list with [the best row, best col, best score]
#     """
#     if player == COMP:
#         best = [-1, -1, -infinity]
#     else:
#         best = [-1, -1, +infinity]

#     if depth == 0 or game_over(state):
#         score = evaluate(state)
#         return [-1, -1, score]

#     for cell in empty_cells(state):
#         x, y = cell[0], cell[1]
#         state[x][y] = player
#         score = minimax(state, depth - 1, HUMAN if player == COMP else COMP)
#         state[x][y] = EMPTY_CELL
#         score[0], score[1] = x, y

#         if player == COMP:
#             if score[2] > best[2]:
#                 best = score  # max value
#         else:
#             if score[2] < best[2]:
#                 best = score  # min value

#     return best


def main():
    st.write(
        """
        # ❎⭕ Tic Tac Toe
        """
    )
    if "board" not in st.session_state:
        init()

    reset, _ = st.columns([1, 1])

    reset.button('Restart', on_click=init, args=(True,))
    if st.session_state.player == COMP and not st.session_state.over:
        computer_player()

    cols = st.columns([55, 55, 55, 55, 55])
    for i, row in enumerate(st.session_state.board):

        for j, field in enumerate(row):
            cols[j+1].button(
                field,
                key=f"{i}-{j}",
                on_click=handle_click,
                args=(i, j),
            )
    check_state()


if __name__ == '__main__':
    main()
