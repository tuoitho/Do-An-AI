import streamlit as st
import numpy as np
import random

def init(post_init=False):
    # if not post_init:
    #     st.session_state.opponent = 'Human'
    st.session_state.win = {'❌': 0, '⭕': 0}
    st.session_state.board = np.full((3, 3), ' ', dtype=str)
    st.session_state.player = '❌'
    st.session_state.warning = False
    st.session_state.winner = None
    st.session_state.over = False


def check_available_moves(extra=False) -> list:
    raw_moves = [row for col in st.session_state.board.tolist() for row in col]
    num_moves = [i for i, spot in enumerate(raw_moves) if spot == ' ']
    if extra:
        return [(i // 3, i % 3) for i in num_moves]
    return num_moves


def check_rows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return None


def check_diagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board) - i - 1] for i in range(len(board))])) == 1:
        return board[0][len(board) - 1]
    return None


def check_state():
    if st.session_state.winner:
        st.success(f"Congrats! {st.session_state.winner} won the game! 🎈")
    if st.session_state.warning and not st.session_state.over:
        st.warning('⚠️ This move already exist')
    if st.session_state.winner and not st.session_state.over:
        st.session_state.over = True
        st.session_state.win[st.session_state.winner] = (
            st.session_state.win.get(st.session_state.winner, 0) + 1
        )
    elif not check_available_moves() and not st.session_state.winner:
        st.info(f'It\'s a tie 📍')
        st.session_state.over = True

def check_win(board):
    for new_board in [board, np.transpose(board)]:
        result = check_rows(new_board)
        if result:
            return result
    return check_diagonals(board)



def computer_player():
    moves = check_available_moves(extra=True)
    if moves:
        i, j = make_best_move(st.session_state.board)
        handle_click(i, j)


def handle_click(i, j):
    if (i, j) not in check_available_moves(extra=True):
        st.session_state.warning = True
    elif not st.session_state.winner:
        st.session_state.warning = False
        st.session_state.board[i, j] = st.session_state.player
        st.session_state.player = "⭕" if st.session_state.player == "❌" else "❌"
        winner = check_win(st.session_state.board)
        if winner != " ":
            st.session_state.winner = winner


button_style = """
        <style>
        .stButton > button {
            color: blue;
            width: 90px;
            height: 90px;
            font-size: 20px;
            border-radius:10px;
            padding: 20px;
        }
        </style>
        """
st.markdown(button_style, unsafe_allow_html=True)
def make_best_move(board):
    best_score = -np.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i,j] == ' ':
                board[i,j] = '⭕'
                score = minimax(board, 0, False)
                board[i,j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move
def minimax(board, depth, is_maximizing):
    if check_winner(board, '⭕'):
        return 1
    elif check_winner(board, '❌'):
        return -1
    elif check_game_over(board):
        return 0
    
    if is_maximizing:
        best_score = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i,j] == ' ':
                    board[i,j] = '⭕'
                    score = minimax(board, depth+1, False)
                    board[i,j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = np.inf
        for i in range(3):
            for j in range(3):
                if board[i,j] == ' ':
                    board[i,j] = '❌'
                    score = minimax(board, depth+1, True)
                    board[i,j] = ' '
                    best_score = min(score, best_score)
        return best_score
    

def check_winner(board, player):
    # Check rows and columns
    for i in range(3):
        if (board[i,:] == [player]*3).all() or (board[:,i] == [player]*3).all():
            return True
    
    # Check diagonals
    if (np.diag(board) == [player]*3).all() or (np.diag(np.fliplr(board)) == [player]*3).all():
        return True
    
    return False

# Function to check if the game is over (draw)
def check_game_over(board):
    return (board == ' ').sum() == 0
def main():
    st.write(
        """
        # ❎⭕ Tic Tac Toe
        """
    )
    if "board" not in st.session_state:
        init()

    # Tạo nút New game
    reset, score, player, settings = st.columns([0.5, 0.6, 1, 1])
    reset.button('Restart', on_click=init, args=(True,))
    if st.session_state.player == '⭕' and not st.session_state.over:
        computer_player()
        
    cols = st.columns([55,55,55, 55,55])   
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