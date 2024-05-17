import streamlit as st
import numpy as np
import random
import base64

def create_board():
    return np.zeros((6, 7))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[5][col] == 0

def get_next_open_row(board, col):
    for r in range(6):
        if board[r][col] == 0:
            return r

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

def winning_move(board, piece):
    # Kiểm tra chiều ngang
    for c in range(4):
        for r in range(6):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Kiểm tra chiều dọc
    for c in range(7):
        for r in range(3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Kiểm tra đường chéo từ trên xuống dưới
    for c in range(4):
        for r in range(3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Kiểm tra đường chéo từ dưới lên trên
    for c in range(4):
        for r in range(3, 6):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opp_piece = 1 if piece == 2 else 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    # Đánh giá cột giữa
    center_array = [int(i) for i in list(board[:, 3])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Đánh giá chiều ngang
    for r in range(6):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(4):
            window = row_array[c:c+4]
            score += evaluate_window(window, piece)

    # Đánh giá chiều dọc
    for c in range(7):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # Đánh giá đường chéo từ trên xuống dưới
    for r in range(3):
        for c in range(4):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Đánh giá đường chéo từ dưới lên trên
    for r in range(3):
        for c in range(4):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

def get_valid_locations(board):
    valid_locations = []
    for col in range(7):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, 2):
                return (None, 100000000000000)
            elif winning_move(board, 1):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, 2))  # Đánh giá vị trí từ góc độ của máy
    
    if maximizing_player:
        value = -np.Inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 2)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Alpha-Beta Pruning
        return column, value
    
    else:  # minimizing player
        value = np.Inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, 1)
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if beta <= alpha:
                break  # Alpha-Beta Pruning
        return column, value



def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0


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

def init():
    return st.selectbox("Select column (0-6):", options=list(range(7)))
    
def connect_four():
    state = st.session_state
    if 'board' not in state:
        state.board = create_board()
        state.game_over = False
        state.turn = 0
        state.is_ai_turn = False  # Thêm biến boolean để chỉ định lượt AI

    st.title("Connect Four")
    selected_col = init()

    if st.button("New Game"):
        state.board = create_board()
        state.turn = 0
        state.game_over = False
        state.is_ai_turn = False  # Reset biến lượt AI khi bắt đầu trò chơi mới

    if st.button("Drop piece"):
        if is_valid_location(state.board, selected_col) and not state.game_over:
            row = get_next_open_row(state.board, selected_col)
            if state.turn == 0:
                drop_piece(state.board, row, selected_col, 1)
                if winning_move(state.board, 1):
                    st.write("Player wins!")
                    state.game_over = True
            else:
                col, minimax_score = minimax(state.board, 4, -np.Inf, np.Inf, True) # Độ sâu của Minimax là 4
                row = get_next_open_row(state.board, col)
                drop_piece(state.board, row, col, 2)
                if winning_move(state.board, 2):
                    st.write("AI wins!")
                    state.game_over = True
                elif len(get_valid_locations(state.board)) == 0:
                    st.write("It's a tie!")
                    state.game_over = True
                state.is_ai_turn = False  # Đánh dấu lượt của AI đã kết thúc

            state.turn += 1
            state.turn = state.turn % 2

    # Sử dụng hàm callback để tự động thực hiện lượt đánh của AI
    if state.is_ai_turn and not state.game_over:
        col, _ = minimax(state.board, 4, -np.Inf, np.Inf, True)  # AI chọn cột
        row = get_next_open_row(state.board, col)
        drop_piece(state.board, row, col, 2)
        if winning_move(state.board, 2):
            st.write("AI wins!")
            state.game_over = True
        elif len(get_valid_locations(state.board)) == 0:
            st.write("It's a tie!")
            state.game_over = True
        state.is_ai_turn = False  # Đánh dấu lượt của AI đã kết thúc

    st.write(np.flip(state.board, 0))
    st.session_state['board'] = state.board  # Lưu trạng thái của board vào session state

    if state.game_over:
        st.balloons()


connect_four()
