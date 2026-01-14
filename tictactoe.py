import tkinter as tk
import random
import math

root = tk.Tk()
root.title("Tic Tac Toe")
root.configure(bg="#f2f2f2")

board = [" " for _ in range(9)]
buttons = []
game_over = False

player_starts = True  # 🔑 KEY VARIABLE
difficulty = tk.StringVar(value="Easy")

WIN_COMBOS = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

status = tk.Label(root, text="Your Turn (X)", font=("Arial", 16), bg="#f2f2f2")
status.grid(row=0, column=0, columnspan=3, pady=10)

difficulty_menu = tk.OptionMenu(root, difficulty, "Easy", "Medium", "Hard")
difficulty_menu.config(font=("Arial", 12))
difficulty_menu.grid(row=1, column=0, columnspan=3)

# ---------------- LOGIC ----------------
def check_winner(b, p):
    for c in WIN_COMBOS:
        if b[c[0]] == b[c[1]] == b[c[2]] == p:
            return True
    return False

def is_full(b):
    return " " not in b

# ---------- MINIMAX ----------
def minimax(b, is_max):
    if check_winner(b, "O"):
        return 1
    if check_winner(b, "X"):
        return -1
    if is_full(b):
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                best = max(best, minimax(b, False))
                b[i] = " "
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                best = min(best, minimax(b, True))
                b[i] = " "
        return best

# ---------- AI MOVES ----------
def easy_move():
    return random.choice([i for i in range(9) if board[i] == " "])

def medium_move():
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            if check_winner(board, "O"):
                board[i] = " "
                return i
            board[i] = " "
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            if check_winner(board, "X"):
                board[i] = " "
                return i
            board[i] = " "
    if board[4] == " ":
        return 4
    return easy_move()

def hard_move():
    best, move = -math.inf, None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best:
                best, move = score, i
    return move

def computer_move():
    global game_over
    if game_over:
        return

    move = (
        easy_move() if difficulty.get() == "Easy"
        else medium_move() if difficulty.get() == "Medium"
        else hard_move()
    )

    board[move] = "O"
    buttons[move].config(text="O", state="disabled")

    if check_winner(board, "O"):
        status.config(text="Computer Wins!")
        game_over = True
        disable_all()
    elif is_full(board):
        handle_draw()
    else:
        status.config(text="Your Turn (X)")

def player_move(i):
    global game_over
    if board[i] != " " or game_over:
        return

    board[i] = "X"
    buttons[i].config(text="X", state="disabled")

    if check_winner(board, "X"):
        status.config(text="You Win!")
        game_over = True
        disable_all()
    elif is_full(board):
        handle_draw()
    else:
        status.config(text="Computer's Turn (O)")
        root.after(300, computer_move)

def handle_draw():
    global game_over, player_starts
    status.config(text="It's a Draw!")
    game_over = True
    player_starts = not player_starts  # 🔁 SWITCH TURN
    disable_all()

def disable_all():
    for b in buttons:
        b.config(state="disabled")

def restart():
    global game_over
    game_over = False
    for i in range(9):
        board[i] = " "
        buttons[i].config(text=" ", state="normal")

    if player_starts:
        status.config(text="Your Turn (X)")
    else:
        status.config(text="Computer Starts (O)")
        root.after(300, computer_move)

# ---------------- GRID ----------------
for i in range(9):
    btn = tk.Button(
        root, text=" ", font=("Arial", 24, "bold"),
        width=5, height=2, bg="white",
        command=lambda i=i: player_move(i)
    )
    btn.grid(row=(i//3)+2, column=i%3, padx=5, pady=5)
    buttons.append(btn)

tk.Button(
    root, text="Restart", font=("Arial", 12),
    bg="#4CAF50", fg="white", command=restart
).grid(row=5, column=0, columnspan=3, pady=15)

root.mainloop()
