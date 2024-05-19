from math import inf as infinity
from random import choice
import base64
import time
import numpy as np
import streamlit as st
from streamlit.components.v1 import html



st.session_state.HUMAN = '❌'
st.session_state.COMP = '🟢'
EMPTY_CELL = ' '
st.session_state.mode="Hard"
st.sidebar.markdown(
    """
    <div class="red-text">
        <b style="font-size: 40px;">Welcome to our project </b>
   	<div>
        <p>Advisor: </b>ThS.Trần Tiến Đức </p>
        <p>Email:<a style="color:green" href="ductt@hcmute.edu.vn"> ductt@hcmute.edu.vn</a></p>
         <p><b style="font-size: 40px;">Our team:</b></p>
        <div>
    </p>
        Full name: Lê Đình Trí</p>
        ID: 22110442 </p>
    </p>
        Full name: Liên Huệ Tiên</p>
        ID: 22110433 </p>
    HCM University Technology and Education
        </div>
	<p><b style="font-size: 40px;">Contact with:</b></p>
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
        <p>Phone: <a style="color:green" href="">0362092749</a></p>
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

def init(start=st.session_state.HUMAN):
    st.balloons()
    st.balloons()

    st.session_state.win = {st.session_state.HUMAN: 0, st.session_state.COMP: 0}
    st.session_state.board = np.full((3, 3), EMPTY_CELL, dtype=str)
    st.session_state.player = start
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
    # print("Computer's turn")
    depth = len(empty_cells(st.session_state.board))
    if depth == 0 or game_over(st.session_state.board):
        return
    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
        handle_click(x, y)
    else:
        if st.session_state.mode=="Easy":
            move = choice(empty_cells(st.session_state.board))
            x, y = move[0], move[1]
            handle_click(x, y)
        else:
            move = minimax(st.session_state.board, depth, st.session_state.COMP)
            x, y = move[0], move[1]
            handle_click(x, y)
    


def handle_click(i, j):
    if [i, j] not in empty_cells(st.session_state.board):
        st.session_state.warning = True
    elif not st.session_state.winner:
        st.session_state.warning = False
        st.session_state.board[i, j] = str(st.session_state.player)
        # print("1",st.session_state.player)

        st.session_state.player = st.session_state.COMP if st.session_state.player == st.session_state.HUMAN else st.session_state.HUMAN
        # print("2",st.session_state.player)

        winner = st.session_state.HUMAN if wins(st.session_state.board, st.session_state.HUMAN) else st.session_state.COMP if wins(
            st.session_state.board, st.session_state.COMP) else None
        if winner != None:
            st.session_state.winner = winner
    print(st.session_state.player)
    if st.session_state.player == st.session_state.COMP and not st.session_state.over:
        computer_player()


button_style = """
        <style>
        .stButton > button {
            color: black;
            width: 90px;
            height: 90px;
            font-size: 20px;
            border-radius:20px;
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
    if wins(state, st.session_state.COMP):
        score = +1
    elif wins(state, st.session_state.HUMAN):
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
    return wins(state, st.session_state.HUMAN) or wins(state, st.session_state.COMP)


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
        score = minimax(state, depth - 1, st.session_state.HUMAN if player ==
                        st.session_state.COMP else st.session_state.COMP, alpha, beta)
        if wins(state,st.session_state.COMP):
            state[x][y] =' '
            score[0],score[1]=x,y
            return score
        state[x][y] = EMPTY_CELL
        if player == st.session_state.COMP:
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

    if player == st.session_state.COMP:
        return [row, col, alpha]
    else:
        return [row, col, beta]

st.markdown("""
	<style>
	.stSelectbox:first-of-type > div[data-baseweb="select"] > div {
	      background-color: yellow;
    	      padding: 20px;
        font-size: 20px;
        font-weight: bold;
	}
	</style>
""", unsafe_allow_html=True)



   

def main():
    st.write(
        """
        # ❎🔴 Tic Tac Toe
        """
    )
    if "board" not in st.session_state:
        init()
    col1,col2,col3=st.columns([1,1,2])
    with col1:
        di_truoc=st.selectbox("Chọn người chơi đi trước",["HUMAN","PC"])
    with col2:
        chon_ki_hieu_human = st.selectbox("Chọn kí hiệu của bạn",["❌","🟢"])
    with col3:
        mode=st.selectbox("Chọn chế độ chơi",["Hard(using Minimax)","Easy"])
    _,colmid,_=st.columns([1,1,1])
    with colmid:
        OK = st.button("Apply",type="primary")
    if chon_ki_hieu_human == "❌":
        st.session_state.HUMAN = '❌'
        st.session_state.COMP = '🟢'
    else:
        st.session_state.HUMAN = '🟢'
        st.session_state.COMP = '❌'

    

    if OK:
        if mode == "Easy":
            st.session_state.mode="Easy"
        else:
            st.session_state.mode="Hard"
        if di_truoc == "HUMAN":
            init()
            st.session_state.player = st.session_state.HUMAN
        else:
            init()
            st.session_state.player = st.session_state.COMP
            computer_player()



    cols = st.columns([1, 1, 1, 1, 1,1])
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
