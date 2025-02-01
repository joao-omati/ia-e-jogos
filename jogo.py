import tkinter as tk
from tkinter import messagebox

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    
    return False

def available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def minimax(board, depth, is_maximizing):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if not available_moves(board):
        return 0
    
    if is_maximizing:
        best_score = -float("inf")
        for (r, c) in available_moves(board):
            board[r][c] = "O"
            score = minimax(board, depth + 1, False)
            board[r][c] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for (r, c) in available_moves(board):
            board[r][c] = "X"
            score = minimax(board, depth + 1, True)
            board[r][c] = " "
            best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -float("inf")
    move = None
    for (r, c) in available_moves(board):
        board[r][c] = "O"
        score = minimax(board, 0, False)
        board[r][c] = " "
        if score > best_score:
            best_score = score
            move = (r, c)
    return move

def on_click(r, c):
    if board[r][c] == " " and not check_winner(board, "X") and not check_winner(board, "O"):
        board[r][c] = "X"
        buttons[r][c].config(text="X")
        if check_winner(board, "X"):
            messagebox.showinfo("Jogo da Velha", "Você venceu!")
            return
        if not available_moves(board):
            messagebox.showinfo("Jogo da Velha", "Empate!")
            return
        
        move = best_move(board)
        if move:
            board[move[0]][move[1]] = "O"
            buttons[move[0]][move[1]].config(text="O")
        
        if check_winner(board, "O"):
            messagebox.showinfo("Jogo da Velha", "A IA venceu!")
        elif not available_moves(board):
            messagebox.showinfo("Jogo da Velha", "Empate!")

def reset_game():
    global board
    board = [[" " for _ in range(3)] for _ in range(3)]
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text=" ")

root = tk.Tk()
root.title("Jogo da Velha")
board = [[" " for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]

for r in range(3):
    for c in range(3):
        buttons[r][c] = tk.Button(root, text=" ", font=("Arial", 24), width=5, height=2, command=lambda r=r, c=c: on_click(r, c))
        buttons[r][c].grid(row=r, column=c)

tk.Button(root, text="Reiniciar", font=("Arial", 14), command=reset_game).grid(row=3, column=0, columnspan=3)
root.mainloop()
